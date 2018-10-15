"""
The name of this script is no longer appropriate. This script uses PyGrace to
make plots of the fit cuts, which have been informed by the weigh-in gaps. This
script takes a single argument, the minimum number of weigh-ins that you wish to
include in the analysis. For example, this will run the analysis and generate
the plots for all users who have 400 or more weigh-ins:

 python plot-freq-vs-fit-cuts.py 400

"""
#########
# Setup #
#########

N_plots_per_panel = 15

# Set up the database connection:
from database import *   # module in PYTHONPATH
database = "calorie_king_social_networking_2010"  
server   = "tarraco.chem-eng.northwestern.edu"
user     = "calorieking" 
passwd   = "n1ckuDB!"
db       = Connection(server, database, user, passwd) 

# Get the number of weigh-ins from the scrip's command-line invocation
import sys
if len(sys.argv) < 2:
    raise AssertionError('You must provide a minimum number of weigh-ins')
N_weigh_ins = sys.argv[1]

# Get a list of applicable users sorted by decreasing variance. The return value
# from this query is a list of dictionaries.
count_query_list = db.query("""
	SELECT
		C.ck_id,
		C.n_weigh_ins / MSE.mse AS variance
	FROM
		weigh_in_counts C
		JOIN (
			SELECT ck_id, sum(quality) AS mse
			FROM weigh_in_cuts
			GROUP BY ck_id
		) MSE
		ON (C.ck_id = MSE.ck_id)
	WHERE C.n_weigh_ins > %s
	ORDER BY variance DESC

""" % (N_weigh_ins))
# This is the old query that didn't pay attention to the variance:
#    SELECT ck_id
#    FROM weigh_in_counts
#    WHERE n_weigh_ins >= %s

# Kick out bad users:               --> skipping this for now
#import baduserslist

# Make sure we got at least one user:
if len(count_query_list) == 0:
    raise ValueError('Did not get any users with more than %s weigh-ins' % (N_weigh_ins))

# The on_day values are datetime objects, and we'll need to do some arithmetic
from datetime import *

# Needed to compute the curve for the exponential fit:
import math

# Needed, obviously, for plotting
from PyGrace.grace import Grace
from PyGrace.Styles.el import *

# Create multi-panel pages:
from PyGrace.Extensions.panel import Panel, MultiPanelGrace

########################################
# A function that creates output files #
########################################
# The resulting individual postscript files are eventually concatenated into
# one large file; this simply generates one file per page.

def make_output_for (grace, panel):
#    for g in grace.graphs:
#    	g.world.ymax = 500
    grace.automulti(width_to_height_ratio=1.0,hgap=0.05,vgap=0.15,
                hoffset=(0.1,0.05),voffset=(0.05,0.1))
    grace.scale_suffix(0.3,"major_size")
    grace.scale_suffix(0.3,"minor_size")
    grace.scale_suffix(0.3,"char_size")
    grace.write_file('%03d.ps' % panel)
    
n_plots_this_panel = 0
n_panels = 0
grace = MultiPanelGrace()

##################################
# Loop over all applicable users #
##################################

for count_query in count_query_list:
    n_plots_this_panel += 1
    ck_id = count_query['ck_id']
    short_id = ck_id[:10]
    
#    # Skip bad users:               --> skipping this for now
#    if (baduserslist.is_bad_user(short_id)):
#        print "Skipping %s: %s" % (short_id,baduserslist.why_bad_user(short_id))
#        continue
    
    print "Working with user %s (%s); variance %f" % \
        (short_id, ck_id, count_query['variance'])
    
    # Create the graph object and set the (sub)title
    graph = grace.add_graph(Panel)
    graph.subtitle.text = str(short_id)
    graph.subtitle.size = 1
    
    # Set the x and y axes to decimal format (rather than scientific notation)
    graph.xaxis.ticklabel.configure(format='decimal')
    graph.yaxis.ticklabel.configure(format='decimal')
    
    ####################################
    # Pull the actual time series data #
    ####################################
    
    time_series = db.query("""
        SELECT on_day,weight
        FROM weigh_in_history
        WHERE ck_id = "%s"
        ORDER BY on_day
    """ % (ck_id))
    
    # Calculate the 'days since first weigh-in'
    days = [entry['on_day'] for entry in time_series]
    first_day = days[0]
    days = [int((day - first_day).days) for day in days]
    
    # Calculate the percentage weight change
    weights = [entry['weight'] for entry in time_series]
    # Get the first nonzero weight. Not a problem if we've removed zeroes,
    # but here in case we decide to view such time series:
    first_weight = [w for w in weights if w > 0][0]
    pct_changes = [(w - first_weight) / first_weight * 100 for w in weights]
    # Filter out weigh-ins of zero weight, or enormous values:
    #t_series = filter(lambda x: x[1] > -100 and x[1] < 200, zip (days, pct_changes))
    t_series = zip (days, pct_changes)
    
    ####################################
    # Shaded background indicates gaps #
    ####################################
    
    freq_cuts = db.query("""
        SELECT start_day,end_day
        FROM gaps_by_frequency
        WHERE ck_id LIKE "%s"
        ORDER BY start_day
    """ % (ck_id))
    
    y_max = max(pct_changes)
    for freq_cut in freq_cuts:
        # add a dataset from the upper left to the upper right corner of the
        # grey area:
        background = graph.add_dataset([(freq_cut['start_day'], y_max), \
            (freq_cut['end_day'], y_max)], legend = '')
        background.symbol.shape   = 0  # no symbols
        background.line.style     = 0  # hide lines ...
        background.line.pattern   = 0  # ... leave ...
        background.line.color     = 1  # ... only ...
        background.line.linewidth = 1  # ... shades
        
        # This sets the filling type as "to_baseline", baseline as "x-axis" and
        # shade color as lightgrey
        background.fill.type = 2
        background.fill.color = 7 # lightgrey
        background.baseline.type = 3
    
    ###############################
    # Plot the actual time series #
    ###############################
    
    # Add the data to the graph
    dataset = graph.add_dataset(t_series, ElCircleDataSet, 1)
    dataset.symbol.size = 0.2
    graph.autoscale()
    
    
    ###################
    # The fit results #
    ###################
    
    # Plot the fit curves using alternating colors
    fits = db.query("""
        SELECT fit_type,start_day,stop_day,param1,param2,param3,quality
        FROM weigh_in_cuts
        WHERE ck_id = "%s"
        ORDER BY start_day
    """ % (ck_id))
    
    line_color = 2  # alternate line colors
    
    for fit in fits:
        # draw lines/curves for linear/exponential fits
        xs = range (fit['start_day'], fit['stop_day'])
        if fit['fit_type'] == 'lin':
            ys = [fit['param1'] + fit['param2'] * x for x in xs];
        else:
            ys = [fit['param1'] + fit['param2'] * math.exp(x * fit['param3']) \
                for x in xs];
        
        fit_curve = graph.add_dataset(zip (xs, ys), ElLineDataSet, line_color)
        fit_curve.line.configure(linewidth = 2.0)
        
        # Alternate colors:
        line_color = 3 if line_color == 2 else 2
        
    ###########################
    # Force a common y extent #
    ###########################
    
    # Make all graphs have a y-extent of at least 40
    y_min = min(pct_changes)
    y_max = max(pct_changes)
    if y_max - y_min < 30:
        extra = 30 - (y_max - y_min)
        graph.world.ymin = y_min - extra/2
        graph.world.ymax = y_max + extra/2
    
    
    
    ############################
    # Save the panel to a file #
    ############################

    if n_plots_this_panel == 15:
        # print the grace to a file (.agr format)
        n_panels += 1
        make_output_for(grace, n_panels)
        # Set up the grace object for the next round
        n_plots_this_panel = 0
        grace = MultiPanelGrace()

# Finish by flushing out the last panel if it has any plots
if n_plots_this_panel > 0:
    n_panels += 1
    make_output_for(grace, n_panels)

#######################################
# Finally, merge all the panel images #
#######################################

import subprocess
# Merge the ps files
subprocess.call("psmerge -oimages.ps [0-9][0-9][0-9].ps", shell=True)   # merge all individuals pages into a single figure
# Remove individual .ps files
subprocess.call("rm [0-9][0-9][0-9].ps", shell=True)  # remove all individual figures-pages

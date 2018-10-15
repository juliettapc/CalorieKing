from look_up_table import *
import itertools

activity = activity_table()
look_up = look_up_table()

x = [x.strip().split(" ,")[0] for x in \
open("./method3/csv/nonadherent_not_networked_pwl.csv").readlines()]

y = [y.strip().split(" ,")[0] for y in \
open("./method3/csv/adherent_not_networked_pwl.csv").readlines()]

print "check adherent", len(x)
print "check nonadherent", len(y)

ius = list(itertools.chain(*[x,y]))
print ius
ius = map(int,ius)

f = open("./method3/csv/engaged_not_networked_act_wi_ibmi.csv","w")
print>>f, ",".join(["pwc","act","wi","ibmi", "time_in_sys"])

ov_ob = []
#select overweight and obese ius
for n in ius:
    if float(look_up["initial_BMI"][n])>=25:
        ov_ob.append(n)

for n in ov_ob:
    t = (look_up["percentage_weight_change"][n],activity["activity"][n],look_up["weigh_ins"][n],look_up["initial_BMI"][n],
    look_up["time_in_system"][n])
    print t
    print>>f,",".join(map(str,t))

f.close()

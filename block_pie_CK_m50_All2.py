"""
block_comm_CK_wedge_curve.py

Created by Satyam Mukherjee on 2011-07-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.

Plot the communities and blocks for small components and also non-networked group using pie-charts. 
"""
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import string
import random
import numpy as np
from matplotlib import pyplot, mpl
from matplotlib.colors import LogNorm
from math import pi,sin,cos,sqrt
import pylab
from matplotlib.patches import Wedge, Polygon
import matplotlib.ticker as ticker
from matplotlib.widgets import Slider, Button
#import nx_pylab2 as nx2
from matplotlib.patches import FancyArrowPatch, Circle
#from colorsnew import cmap_discretize
import matplotlib as m




graph_name1 = "method2_50/networks/method2_50_adherent.gml"      ### Method3

G = nx.read_gml(graph_name1)
G = nx.connected_component_subgraphs(G)[0]
listsort1 =  [[u'38481', u'40842', u'46549', u'17427', u'41063', u'7264', u'35755', u'16584', u'42825', u'39816', u'28627', u'44291', u'36915', u'38164', u'2573', u'30898', u'43373', u'45655', u'38629', u'46451', u'46254', u'45064', u'39167', u'39953', u'39600', u'43282', u'3753', u'30300', u'38798', u'45392', u'36268', u'45758', u'32683', u'34064', u'32242', u'46601', u'4094', u'32108', u'46118', u'38479', u'35766'], [u'18956', u'39714', u'27171', u'46480', u'4655', u'41720', u'41906', u'3869', u'27995', u'45364', u'38641', u'14142', u'29881', u'39252', u'28743', u'41480', u'5842', u'33422', u'36783', u'35561', u'20494', u'6137', u'43821', u'29802', u'42270', u'39823', u'23012', u'20972', u'22783', u'29540', u'28308', u'46643', u'30050', u'4597', u'28945', u'7330', u'18531', u'45676', u'33143', u'27847', u'3217', u'43334', u'29250', u'27127', u'32340', u'46600', u'15479', u'4455', u'11729', u'35309', u'44916'], [u'42877', u'5820', u'42380', u'42510', u'3144', u'35059', u'14867', u'29053', u'33282', u'24629', u'44334', u'41561', u'46162', u'5536', u'46271', u'44757', u'31246', u'42348', u'39055', u'41851', u'8034', u'46721', u'41225', u'41165', u'29376', u'39770', u'32508', u'18656', u'44449', u'38029', u'40653', u'34754', u'41261', u'5613', u'17086', u'45916', u'41728', u'32395', u'27851', u'41745', u'40296', u'42000', u'42401', u'42087', u'34450', u'46663', u'32892', u'24642', u'28118', u'20377', u'45922', u'32637', u'45190', u'4800', u'43617', u'17097', u'46389', u'29314', u'41999', u'29480', u'44188', u'40476', u'36088', u'36343', u'45154'], [u'44121', u'3557', u'41794', u'24308', u'967', u'43573', u'47061', u'43981', u'24575', u'41830', u'21994', u'44866', u'46798', u'9486', u'15389', u'42637', u'46315', u'45116', u'41049', u'20553', u'41656', u'37258', u'36157', u'42467', u'7073', u'46612', u'45795', u'38044', u'9831', u'42765', u'6322', u'46998', u'12252', u'36591', u'41509', u'17484', u'80', u'19515', u'46496', u'2832', u'14722', u'40854', u'29840', u'46782', u'42807', u'8371', u'45303', u'17755', u'15311', u'43437', u'45374', u'45771', u'32214', u'33340', u'30166', u'43252', u'21010', u'12048', u'12484', u'3719', u'37781', u'46026', u'36865', u'998', u'39130', u'44265', u'310', u'44263', u'23266', u'26102', u'45298', u'10127', u'833', u'13662', u'41669', u'18106', u'19501', u'10542', u'29018', u'29930', u'44884', u'36255', u'36701', u'25991', u'13790', u'3864', u'42886', u'36411', u'35493', u'43435', u'28845', u'46582', u'29070', u'18647', u'33242', u'17923', u'38945', u'9429', u'18790', u'43402', u'40232', u'8997', u'19311', u'8638', u'36351', u'24180', u'42911', u'35135', u'39485', u'45670', u'25619', u'17369', u'36917', u'32662', u'31021', u'38972', u'43442', u'13518', u'30372', u'29826', u'10924', u'29415', u'43150', u'42384', u'16541', u'45557', u'40582', u'21215', u'10378', u'40402', u'27756', u'3424'], [u'33322', u'28851', u'13739', u'39065', u'39898', u'33425', u'3284', u'32833', u'38955', u'41792', u'35531', u'44195', u'44199', u'42457', u'43572', u'37747', u'32167', u'3815', u'27301', u'42484', u'42585', u'40520', u'40443', u'34221', u'45437', u'5817', u'39690', u'10411', u'46941', u'34752', u'37000', u'38315', u'36925', u'41510', u'41160', u'38914', u'39155', u'6613', u'41194', u'45060', u'44166', u'41584', u'20312', u'40324', u'40803', u'27345', u'40484', u'31124', u'5068', u'6627', u'26718', u'38101', u'47043', u'27958', u'5580', u'41899', u'42608', u'31513', u'2158', u'45833', u'47038', u'41095', u'18967', u'35849', u'45148', u'40734', u'43192', u'45903', u'46121', u'40027', u'19708', u'12992', u'36237', u'42022', u'40284', u'45243', u'31547', u'39006', u'46785', u'45876', u'33441', u'46878', u'19', u'31425', u'42156', u'45009', u'29371', u'41292', u'18654', u'43953', u'14378', u'42471', u'27811', u'14376', u'19000', u'19943', u'29592', u'39342', u'40719', u'17258', u'28050', u'12798', u'41316', u'45220', u'45061', u'45784', u'46234', u'42612', u'42971', u'33717', u'32811', u'44214', u'43858', u'45760', u'33372', u'47067', u'30570', u'43848', u'31383', u'39017', u'40138', u'32171', u'43138', u'29399', u'46148', u'39978', u'33369', u'43177', u'30392', u'42714', u'28301', u'41553', u'36726', u'6197', u'45860', u'46689', u'9816', u'17598', u'37574', u'45261', u'35955', u'46326', u'18541', u'34955', u'42225', u'44352', u'19546', u'43401', u'4336', u'31076', u'29749', u'39948', u'36631', u'46329', u'45139', u'39478', u'28436', u'17857', u'11477', u'45513', u'46639', u'41435', u'39688', u'33062', u'1055', u'36529', u'41987', u'11926', u'34061', u'3944', u'13136', u'43446', u'10915', u'41187', u'12977', u'32349', u'20327', u'39383', u'42550', u'39971', u'41521', u'41970', u'28212', u'28688', u'36719', u'12115', u'45419', u'42319', u'42317', u'47052', u'31353', u'39809', u'27759', u'37143', u'37639', u'45527'], [u'35544', u'41015', u'12486', u'41371', u'41797', u'41559', u'39625', u'37188', u'45933', u'29453', u'46487', u'13731', u'46726', u'43599', u'43982', u'12013', u'40844', u'19450', u'46439', u'46269', u'39539', u'44169', u'39313', u'11613', u'10959', u'44791', u'32476', u'35274', u'35973', u'31391', u'40188', u'31954', u'20411', u'41586', u'19022', u'41769', u'47063', u'42018', u'43542', u'31826', u'46046', u'43541', u'46347', u'43543', u'614', u'41942', u'6390', u'39250', u'42263', u'42262', u'37648', u'42065', u'46533', u'26900', u'28182', u'15367', u'45175', u'38900', u'44614', u'41092', u'35847', u'44571', u'44570', u'32571', u'391', u'4046', u'46123', u'39003', u'40218', u'46613', u'18061', u'1432', u'33895', u'46153', u'27724', u'39022', u'26136', u'30067', u'45470', u'8592', u'31337', u'11313', u'26528', u'13803', u'46771', u'33161', u'18842', u'45379', u'2697', u'44539', u'44021', u'14977', u'31949', u'43318', u'22520', u'27101', u'39673', u'41131', u'40802', u'32915', u'37287', u'12681', u'42358', u'42574', u'37763', u'37600', u'30244', u'25486', u'36369', u'215', u'40656', u'4477', u'42419', u'29115', u'2464', u'41781', u'29522', u'10684', u'22711', u'30359', u'6568', u'46230', u'45506', u'43178', u'41401', u'13228', u'41310', u'28640', u'22903', u'44213', u'32741', u'29467', u'6933', u'39018', u'39019', u'44662', u'259', u'36222', u'7077', u'27511', u'32085', u'11427', u'42399', u'33985', u'39862', u'40666', u'46668', u'34775', u'5295', u'28719', u'20392', u'9590', u'34579', u'39207', u'28169', u'42146', u'44682', u'40161', u'43084', u'26751', u'39111', u'39059', u'44636', u'36176', u'41847', u'32700', u'42240', u'20206', u'28506', u'36330', u'11149', u'20527', u'40545', u'40782', u'18992', u'28342', u'34107', u'27575', u'30917', u'40434', u'3940', u'40539', u'45511', u'5564', u'39422', u'46819', u'47019', u'5286', u'39686', u'46812', u'30964', u'41242', u'44554', u'40052', u'6161', u'12449', u'36629', u'46062', u'45368', u'6883', u'33964', u'42418', u'13511', u'39438', u'727', u'29418', u'30264', u'43020', u'34065', u'17458', u'27973', u'45411', u'46772', u'42716', u'46850', u'47053', u'6083', u'25318', u'40811', u'32116', u'45528', u'34141', u'41203'], [u'36585', u'27490', u'40155', u'27284', u'27280', u'46820', u'39656', u'28854', u'43112', u'36092', u'32233', u'40929', u'41479', u'41373', u'37041', u'44855', u'19701', u'38954', u'30192', u'2915', u'41650', u'38959', u'41790', u'7129', u'28035', u'39624', u'46824', u'6651', u'41152', u'36611', u'43778', u'45545', u'29284', u'43807', u'21108', u'30776', u'39400', u'41724', u'39361', u'39364', u'42054', u'14694', u'43698', u'42053', u'43695', u'39567', u'28404', u'43053', u'40847', u'31778', u'29917', u'29031', u'29033', u'29527', u'43142', u'34110', u'45160', u'40037', u'27711', u'45702', u'33946', u'45565', u'42636', u'45569', u'36332', u'1930', u'45288', u'42227', u'45443', u'39693', u'35379', u'36819', u'5131', u'42226', u'18163', u'46891', u'28664', u'41331', u'39224', u'31487', u'44018', u'20418', u'29086', u'6758', u'29247', u'43307', u'7519', u'27132', u'27137', u'39032', u'43490', u'29962', u'43499', u'37755', u'43941', u'34270', u'45941', u'4030', u'38953', u'46042', u'27574', u'30154', u'41067', u'43394', u'27342', u'30741', u'37874', u'36376', u'27610', u'29662', u'28361', u'4916', u'40247', u'7189', u'27933', u'30736', u'2536', u'42063', u'27836', u'31461', u'47046', u'45627', u'30951', u'9813', u'39189', u'39811', u'36473', u'12375', u'4393', u'44835', u'6578', u'38214', u'46585', u'35201', u'41419', u'45050', u'44111', u'31067', u'33489', u'28601', u'45831', u'46029', u'19063', u'37424', u'39706', u'42116', u'33436', u'36115', u'2901', u'33549', u'40733', u'43865', u'46915', u'1067', u'44184', u'28335', u'43462', u'43461', u'27385', u'40146', u'37228', u'44527', u'43740', u'37617', u'32164', u'35930', u'43582', u'34341', u'28414', u'39411', u'41736', u'28793', u'43995', u'42029', u'42434', u'42432', u'44377', u'40853', u'43041', u'45173', u'28383', u'8316', u'45049', u'36991', u'40455', u'45573', u'36308', u'39301', u'34771', u'19476', u'2112', u'45476', u'39604', u'45656', u'41291', u'46655', u'4699', u'42527', u'46803', u'28775', u'39402', u'42150', u'30803', u'44385', u'7258', u'16058', u'40229', u'46809', u'13719', u'45099', u'39120', u'44158', u'40102', u'39044', u'3989', u'43890', u'29874', u'46180', u'32328', u'28516', u'45895', u'29476', u'46119', u'43009', u'41680', u'40777', u'40958', u'41689', u'30058', u'17578', u'46621', u'38893', u'29988', u'32039', u'43674', u'33960', u'45435', u'14475', u'37115', u'40252', u'29528', u'37111', u'46453', u'46020', u'31574', u'22923', u'44212', u'41929', u'42190', u'3445', u'45508', u'42610', u'40338', u'33493', u'3326', u'43210', u'28838', u'42993', u'36990', u'28890', u'42853', u'44663', u'41081', u'45265', u'37027', u'28387', u'33729', u'32337', u'46359', u'45342', u'32426', u'45610', u'45641', u'38932', u'44060', u'45279', u'44407', u'43434', u'27582', u'27854', u'40821', u'27396', u'40133', u'44103', u'30477', u'40613', u'29495', u'40597', u'44831', u'11864', u'16722', u'45966', u'42035', u'5960', u'43911', u'46412', u'31137', u'31044', u'40466', u'46365', u'46363', u'30000', u'45486', u'45497', u'34175', u'36312', u'35886', u'40501', u'42241', u'28305', u'25688', u'41895', u'28309', u'43812', u'45923', u'38121', u'31151', u'41369', u'45861', u'42947', u'29058', u'40235', u'27978', u'27976', u'27186', u'47060', u'5242', u'39201', u'44105', u'39220', u'42925', u'35812', u'44139', u'20625', u'14901', u'44521', u'41402', u'40603', u'43083', u'39768', u'37378', u'31384', u'43715', u'43717', u'44220', u'36071', u'29272', u'43969', u'2960', u'44353', u'29861', u'38052', u'45556', u'5470', u'42445', u'39442', u'42849', u'11285', u'43403', u'18799', u'44054', u'44037', u'44030', u'33235', u'41140', u'37976', u'4651', u'43813', u'45799', u'43762', u'30761', u'43581', u'40230', u'16468', u'30769', u'31261', u'43662', u'4331', u'40786', u'41807', u'42694', u'5513', u'25458', u'40627', u'2552', u'28022', u'27523', u'45422', u'35819', u'39573', u'30344', u'42590', u'39129', u'31566', u'46921', u'46507', u'7311', u'46881', u'43238', u'31585', u'33530', u'42678', u'6458', u'45077', u'26602', u'43295', u'42180', u'43612', u'38271', u'45330', u'42747', u'46186', u'18462', u'33460', u'43206', u'40999', u'43205', u'46959', u'37030', u'39152', u'32968', u'21754', u'32070', u'5705', u'42589', u'41248', u'39834', u'15726', u'47072', u'39836', u'41508', u'34217', u'38714', u'27798', u'38924', u'22593', u'34841', u'41021', u'42914', u'33665', u'40373', u'16735', u'2908', u'46478', u'41613', u'28473', u'2041', u'42559', u'42009', u'22594', u'27983', u'2362', u'43927', u'40680', u'27330', u'45902', u'30032', u'5369', u'44709', u'32397', u'39444', u'42259', u'42090', u'41693', u'42207', u'1440', u'6025', u'4044', u'37380', u'22613', u'35305', u'40400', u'5738', u'26179', u'41059', u'4849', u'12414', u'42179', u'30395', u'45150', u'35944']] 
#sorted(listcom,key=len)




H=nx.Graph()
wtchange = []
ynode = []

bminode = []
bminodep = []
bminodem = []

bmi = []
bmip = []
bmim = []


wtloss = []
for com in listsort1 :
 xnode = []
 print len(com)
 for comnodes in com :

  for node in G.nodes(data=True) :
    if int(node[1]['label']) == int(comnodes) :
     xnode.append(int(node[1]['id']))
     xnode.sort()
     wtloss.append((float(node[1]['percentage_weight_change'])))
     if -11<= (float(node[1]['percentage_weight_change'])) <= 11 :
      wtchange.append((float(node[1]['percentage_weight_change'])))
#     wtchange.append((float(node[1]['percentage_weight_change'])))

     if (float(node[1]['percentage_weight_change'])) >= 0. :
	bmip.append((float(node[1]['percentage_weight_change'])))
#	bminodep.append((float(node[1]['percentage_weight_change']),G.node[n]['id']))

     if (float(node[1]['percentage_weight_change'])) < 0. :
	bmim.append((float(node[1]['percentage_weight_change'])))
#	bminodem.append((float(node[1]['percentage_weight_change']),G.node[n]['id']))


     bunch = [int(node[1]['id'])]+G.neighbors(int(node[1]['id'])) 
#  print bunch
     Gprime = G.subgraph(bunch)
     H.add_edges_from(Gprime.edges())
 ynode.append(xnode)


maxwtchange = max(wtchange)
minwtchange = min(wtchange)

maxwtchangep = max(bmip)
minwtchangep = min(bmip)

maxwtchangem = max(bmim)
minwtchangem = min(bmim)

#print minwtchange, maxwtchange

fig = plt.figure(figsize=(10,10))

ax = fig.add_axes((0.0,0.0,1.0,1.0))


cdict = {'blue': [(0.0, 0.01568627655506134, 0.01568627655506134),  (1.0, 0.06901961386203766, 0.06901961386203766)], 'green': [(0.0, 0.40784314274787903, 0.40784314274787903), (0.099999999999999978, 0.59607845544815063, 0.59607845544815063), (0.19999999999999996, 0.74117648601531982, 0.74117648601531982), (0.30000000000000004, 0.85098040103912354, 0.85098040103912354), (0.40000000000000002, 0.93725490570068359, 0.93725490570068359), (0.5, 1.0, 1.0), (0.59999999999999998, 0.87843137979507446, 0.87843137979507446), (0.69999999999999996, 0.68235296010971069, 0.68235296010971069), (0.80000000000000004, 0.42745098471641541, 0.42745098471641541), (0.90000000000000002, 0.18823529779911041, 0.18823529779911041), (1.0, 0.0, 0.0)], 'red': [(0.0, 0.0, 0.0), (0.099999999999999978, 0.10196078568696976, 0.10196078568696976), (0.19999999999999996, 0.40000000596046448, 0.40000000596046448),  (0.69999999999999996, 0.99215686321258545, 0.99215686321258545), (0.80000000000000004, 0.95686274766921997, 0.95686274766921997), (0.90000000000000002, 0.84313726425170898, 0.84313726425170898), (1.0, 0.64705884456634521, 0.64705884456634521)]}


cmap = m.colors.LinearSegmentedColormap('my_colormap', cdict, 256)
cax = ax.imshow([wtchange],cmap=cmap,vmin=-11, vmax=11,alpha=1,interpolation="nearest")

nshells=len(ynode)

wtpair2 = []
radpair2 = []
for s in range(nshells) : 
   wtpair = []
   radpair = []
#   print len(ynode[s])
   for n in ynode[s] :
#     weightloss = (float(G.node[n]['percentage_weight_change'])-minwtchange)*1.0/(maxwtchange-minwtchange)
     weightloss = (float(G.node[n]['percentage_weight_change']))
     radius = 0.05 + (float(G.node[n]['percentage_weight_change'])-minwtchange)*1.0/(maxwtchange-minwtchange)

     wtpair.append(float(weightloss))
     wtpair.sort()

     radpair.append(float(radius))
     radpair.sort()
   wtpair2.append(wtpair)
   radpair2.append(radpair)


print max(wtloss), min(wtloss)
### Read the Block model gml

BM=nx.blockmodel(H,ynode)
print BM.nodes()
edge_width = []
edge_pos = []

H3=nx.Graph()
H3.add_edges_from(BM.edges())

for (u,v,d) in BM.edges(data=True) :

     edge_width.append(1. + np.log(d['weight']))
     edge_pos.append((u,v))
edge_width.sort()
edge_pos.sort()


#print H3.nodes()

posBM2 = nx.graphviz_layout(H3,prog='twopi', root = 6,args='')
#posBM2 = nx.spring_layout(BM,iterations=55,weighted=False)
#print posBM2

nx.draw_networkx_edges(H3, posBM2, edgelist=edge_pos, style='solid',alpha=1.0, edge_color = 'black', width = edge_width) ### Draw Straight links

#nx2.draw_networkx_edges(H3, posBM2, edgelist=None, alpha=0.25, edge_color = 'gray', width = edge_width) ### Draw curved links

fracs = {}
radius = {}

for n in range(len(BM)):

  fracs[n] = wtpair2[n]
  rgc = len(fracs[n])
  for n1 in fracs :
   i = -1

   for ps in fracs[n1]:
    i = i + 1
    r1 = np.sqrt(i*1.0/np.pi)
#    print "rgc",r1
   j1 = -1
   for s in fracs[n1]:
    j1 = j1 + 1
#    r = np.sqrt(i*1.0/np.pi)
    color2 = float(s)

#    if i>=1 and i<=2:
#     wedge = Wedge((posBM2[n][0],posBM2[n][1]), r*1, 0, 360, width = r*1, fc=(cmap((float(color2-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))), alpha=1, color = (cmap((float(color2-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))))
#     pylab.gca().add_patch(wedge)

#    print "rgc", rgc
#    if i>2:
    wedge = Wedge((posBM2[n][0],posBM2[n][1]), r1, 270+(360.0/float(rgc))*j1, 270+(360.0/float(rgc))*(j1+1), fc=cmap(((float(color2-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))), alpha=1, color = cmap(((float(color2-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))))
    pylab.gca().add_patch(wedge)

#   if i == len(fracs[n]):
#     r2 = np.sqrt(i*1.0/np.pi)
#     wedge = Wedge((posBM2[n][0],posBM2[n][1]), r2*0.5, 0, 360, width = 0.0, fc='black', alpha=1, color = 'black')
#     pylab.gca().add_patch(wedge)


### Open the small component adherent file !!!
#graph_name2="method2_50/networks/method2_50_adherent.gml"
#Gi1 = nx.read_gml(graph_name2)
#print Gi1.nodes()

#Gi2=nx.connected_component_subgraphs(Gi1)
#H2=nx.Graph()
#for Gi in Gi2[1:]:
# if len(Gi)>0:
#  for u,v in Gi.edges():
#   if u!=v :
#    pathdata1.append((u, v))
#    H2.add_edges_from(Gi.edges())
#nodelist = H2.nodes()
#print "adherent-sc", len(nodelist)

#for n in Gi1.nodes():
#  .append((float(Gi1.node[n]['percentage_weight_change'])))
#weightchange.sort()


fh0=open("method2_50/csv/pwc_sc.dat")
weightchange = []
for line in fh0.readlines() :
  line = line.split()
  weightchange.append(float(line[0]))
weightchange.sort()
rsc = len(weightchange)

j = 0

for n in range(len(weightchange)):
    j = j + 1
    r = np.sqrt(j*1.0/np.pi)

#print "rsc", r
for n in range(len(weightchange)):
#    j = j + 1
#    r = np.sqrt(j*1.0/np.pi)
    color3 = float(weightchange[n])

#    if j>=1 and j<=2:
#     wedge = Wedge((100+posBM2[6][0],posBM2[6][1]), r*1, 0, 360, width = r*1, fc=(cmap((float(color3-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))), alpha=1, color = (cmap((float(color3-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))))
#     pylab.gca().add_patch(wedge)


#    if j>2:
    wedge = Wedge((100+posBM2[6][0],posBM2[6][1]), r*1, 270+(360.0/float(rsc))*n, 270+(360.0/float(rsc))*(n+1), fc=cmap(((float(color3-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))), alpha=1, color = cmap(((float(color3-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))))
    pylab.gca().add_patch(wedge)

#j = 0
#for n in range(len(weightchange)):
#    j = j + 1
#    if j == len(weightchange):
#     r = np.sqrt(j*1.0/np.pi)
#     wedge = Wedge((100+posBM2[6][0],posBM2[6][1]), r*0.5, 0, 360, width = 0.0, fc='black', alpha=1, color = 'black')
#     pylab.gca().add_patch(wedge)

### open the non-networked group files ####
fh1=open("method2_50/csv/pwc_not_networked.dat")
wtlossnn = []
for line in fh1.readlines() :
  line = line.split()
  wtlossnn.append(float(line[0]))
wtlossnn.sort()

 
#print len(wtlossnn)
#print wtloss
maxwtchangenn = max(wtlossnn)
minwtchangenn = min(wtlossnn)

print maxwtchangenn, minwtchangenn, len(wtlossnn)
rnn = len(wtlossnn)
i2 = 0
for n in range(len(wtlossnn)):

    i2 = i2 + 1
    r2 = np.sqrt(i2*1.0/np.pi)
#print "rnn",r2

for n in range(len(wtlossnn)):

#    r = np.sqrt(i2*1.0/np.pi)
    color3 = float(wtlossnn[n])

#    if i2>=1 and i2<=2:
#     wedge = Wedge((200+posBM2[6][0],posBM2[6][1]), r*1, 0, 360, width = r*1, fc=(cmap((float(color3-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))), alpha=1, color = (cmap((float(color3-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))))
#     pylab.gca().add_patch(wedge)


#    if i2>2:
    wedge = Wedge((200+posBM2[6][0],posBM2[6][1]), r2*1, 270+(360.0/float(rnn))*n, 270+(360.0/float(rnn))*(n+1) , fc=cmap(((float(color3-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))), alpha=1, color = cmap(((float(color3-minwtchange))*1.0/(float(abs(maxwtchange-minwtchange))))))
    pylab.gca().add_patch(wedge)

#i2 = 0
#for n in range(len(wtlossnn)):
#    i2 = i2 + 1

#    if i2 == 1*len(wtlossnn):
#     r = np.sqrt(i2*1.0/np.pi)
#     print "half", i2,r
     
#     wedge = Wedge((200+posBM2[6][0],posBM2[6][1]), r*0.5, 0, 360, width = 0.0, fc='black', alpha=1, color = 'black')
#     pylab.gca().add_patch(wedge)

pyplot.rcParams["font.size"] = 22
pyplot.rc('text', usetex=True)
c1=pyplot.colorbar(cax,ticks=[-42, -12.5, -10 , -7.5, -5, -2.5, 0, 2.5, 5.0, 7.5, 10.0,22.0],orientation='horizontal',shrink = 0.55)
c1.ax.set_xticklabels((r"$\leq$ -12.5", "-10.0" , "-7.5", "-5.0", "-2.5", "0.0", "2.5", "5.0", r"$\geq$ 7.5"))

#c1.set_label(" percentage weight-change")
#l,b,w,h = plt.gca().get_position().bounds
#ll,bb,ww,hh = c1.ax.get_position().bounds
#c1.ax.set_position([ll*1.0, b+0.45*h, 0.75*ww, h*0.45])


plt.axis('off')
plt.show()


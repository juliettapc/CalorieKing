 

import sys
import os
from datetime import *
from database import *   #codigo para manejar bases de datos
import math
import numpy
from scipy import stats



def main ():


    database = "calorie_king_social_networking_2010"  
    server="tarraco.chem-eng.northwestern.edu"
    user="calorieking" 
    passwd="n1ckuDB!"
    db= Connection(server, database, user, passwd) 



    query="""select * from users""" 
    result1 = db.query(query)  # is a list of dictionaries



    contador=0
   
    for r1 in result1:   #loop over users
        contador+=1
       
        ck_id=r1['ck_id']
       
        print contador, r1

        query3="select  * from gaps_by_frequency where (ck_id ='"+str(ck_id)+"')  order by start_day asc"
        result3 = db.query(query3)
        
           
        num_gaps=len(result3)

        print "# gaps:",num_gaps,ck_id


        if num_gaps>0:
            for r3 in result3: 

                print r3
                starting_gap=r3['start_date']  
                ending_gap=r3['end_date']   
                trend="gap"                    
                zscore_gap=r3['zscore_gap']    # threshold to consider a gap statistically sifnificant  zs>=3  (imposed like that in: analyze_fr print num_gaps
                raw_input()
                

#########################
          
if __name__== "__main__":

    main()
         
##########################

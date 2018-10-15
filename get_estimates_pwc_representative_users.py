#!/usr/bin/env python


'''
Using the coefficients from the linear regression + Heckman correction  (R)
i plug the values for certain representative users (percentiles in BMI, #R6s and #weih-ins), and i get the estimate percent weight change

Created by Julia Poncela, on October, 2013

'''


def main():
 
#Model:  pwc = A0 + A1*X1 + A2*X2 + A3*X3 


    baseline="YES"

######### 4months:
    coeff_intersect_4m=-2.68227   # from the R analysis
    coeff_ibmi_4m= -0.09122 
    coeff_num_wins_4m= -0.10116 
    coeff_R6s_4m= -0.41977 

    list_errors_4m=[1.27404,0.02209,0.01021,0.06622]
    error_4m=0.   
    if baseline=="YES":
        for element_error in list_errors_4m:
            error_4m += element_error
            print error_4m
    else:
        for i in range(len(list_errors_4m)-1):
            i +=1  # i skip the error associated to the intercept
            error_4m += list_errors_4m[i]
            print error_4m
           

    
    list_iBMI=[26,30,35]     #data 25%, 50 and 75% percentiles
    list_num_w_ins_4m=[3,6,11]
    list_num_R6s=[0,2]
    
    
    
##SUSTITUIR LOS VECTORES DE COEFICIENTES Y ERRORES POR SUS VALORES REALES!!!!



########## 6months:
    coeff_intersect_6m= -0.489264   # from the R analysis
    coeff_ibmi_6m= -0.110176
    coeff_num_wins_6m= -0.098255
    coeff_R6s_6m= -0.634944

    list_errors_6m=[ 1.782432,0.029100,0.009238,0.076557]
    
    
    error_6m=0.
    if baseline=="YES":
        for element_error in list_errors_6m:
            error_6m += element_error
            print error_6m
    else:

        for i in range(len(list_errors_6m)-1):
            i +=1  # i skip the error associated to the intercept
            error_6m += list_errors_4m[i]
            print error_6m
            
    
    list_iBMI=[26,30,35]    
    list_num_w_ins_6m=[2,6,12]
    list_num_R6s=[0,2]





#  Plug values into formula:


    print "4months:"
########## 4 months
    for BMI_element in list_iBMI:
        for num_R6s_element in list_num_R6s:
            for num_wins_element in list_num_w_ins_4m:          
                print " pwc for BMI:", BMI_element, " # w-ins:",num_wins_element," and #R6s:" ,num_R6s_element,"is:",
                if baseline=="YES":
                    pwc=coeff_intersect_4m + coeff_ibmi_4m*BMI_element + coeff_num_wins_4m*num_wins_element + coeff_R6s_4m*num_R6s_element  
                    print pwc,error_4m

                else:
                    pwc= coeff_ibmi_4m*BMI_element + coeff_num_wins_4m*num_wins_element + coeff_R6s_4m*num_R6s_element        
                    print pwc,error_4m




    print "\n6months:"
########## 6 months
    for BMI_element in list_iBMI:
         for num_R6s_element in list_num_R6s:
             for num_wins_element in list_num_w_ins_6m:           
                print "pwc for BMI:", BMI_element, " # w-ins:",num_wins_element," and #R6s:" ,num_R6s_element,"is:    ",
                if baseline=="YES":
                     pwc=coeff_intersect_6m + coeff_ibmi_6m*BMI_element + coeff_num_wins_6m*num_wins_element + coeff_R6s_6m*num_R6s_element
                     print pwc,error_6m
                else:
                     pwc= coeff_ibmi_6m*BMI_element + coeff_num_wins_6m*num_wins_element + coeff_R6s_6m*num_R6s_element
                     print pwc,error_6m


## prop. errors: error sum= error x + error y

##################################################
######################################
if __name__ == '__main__':
  #  if len(sys.argv) > 1:
   #     filename_network1 = sys.argv[1]
    #    filename_network_for_kshell = sys.argv[2]
   
     #   main(filename_network1,filename_network_for_kshell)
    #else:
     #   print "Usage: python script.py path/filename.gml  path/filename_for_kshell.gml"

    
    main()

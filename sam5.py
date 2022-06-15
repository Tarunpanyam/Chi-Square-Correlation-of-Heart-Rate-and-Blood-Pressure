import pandas as pd
import numpy as np

def calculate():
    result='Observed Frequencies of Heart rate & BP are as follows: \n'
    df1 = pd.read_csv("test.csv")
    hranges = [0,59,76]
    size=df1.shape[0]
    x,y = (df1.hr.groupby(pd.cut(df1.hr, hranges,include_lowest=True)).count())
    z = size - (x+y)
    #print(x,y,z)
    result=result+'['+str(x)+' '+str(y)+' '+str(z)+']'+'\n'
    bpranges = [0,59,80]
    a,b = (df1.bp.groupby(pd.cut(df1.bp, bpranges,include_lowest=True)).count())
    c = size - (a+b)
    #print(a,b,c)
    result=result+'['+str(a)+' '+str(b)+' '+str(c)+']'+'\n'
    result=result+'The observed value of Heart rate in between 0-59  : '+str(x)+'\n'
    result=result+'The observed value of Heart rate in between 60-80: '+str(y)+'\n'
    result=result+'The observed value of Heart rate in above   80     : '+str(z)+'\n'
    result=result+'The observed value of BP in between 0-59           : '+str(a)+'\n'
    result=result+'The observed value of BP in between 60-80         : '+str(b)+'\n'
    result=result+'The observed value of BP in above 80                 : '+str(c)+'\n'
    # chi-squared test with similar proportions
    from scipy.stats import chi2_contingency
    from scipy.stats import chi2
    # contingency table
    table = [ [x, y, z],
    [a, b, c]]
    #print(table)
    '''
    The output shows the chi-square statistic, the p-value and the degrees of freedom followed by the expected counts.

    '''
    stat, p, dof, expected = chi2_contingency(table)
    result=result+'Value of Chi-square: '+str(stat)+'\n '
    # interpret test-statistic
    # Find the critical value for 95% confidence at given degree of freedom
    confidence = 0.95
    critical = chi2.ppf(confidence, dof)
    result+='At Confidence Level '+str(confidence*100)+'%\nThe critical value is '+str(critical)+'\n'
    result=result+'----------------------------------------------------\n'
    result+='Confidence=%.3f, critical=%.3f, stat=%.3f\n' % (confidence, critical, stat)
    #print('probability=%.3f, critical=%.3f, stat=%.3f' % (prob, critical, stat))
    #print('Correlation based on probability is as follows:')
    result=result+'Correlation based on probability is as follows: \n'
    if abs(stat) >= critical:
        #print('Dependent (reject H0)')

        result=result+'Since Statistical value is greater than Cirtical value : HR and BP are Dependent on each other (reject H0) \n '
    else:
        #print('Independent (fail to reject H0)')
        result=result+'Since Statistical value is less than Cirtical value : HR and BP are Independent on each other (fail to reject H0) \n '
    # interpret p-value

    alpha = 1.0 - confidence
    result=result+'significance=%.3f, p=%.6f \n' % (alpha, p)
    result=result+'Correlation based on significance is as follows: \n'
    #print('Correlation based on significance is as follows:')
    if p <= alpha:
    #     #print('Dependent (reject H0)')
        result=result+'Since P value is less than significance value : HR and BP are Dependent on each other (reject H0) \n'
    else:
        #print('Independent (fail to reject H0)')
        result=result+'Since P value is greater than significance value : HR and BP are Independent on each other (fail to reject H0) \n'
    
    # calculate coefficient of correlation
    result=result+'---------------Correlation strength---------------- \n'
    df1 = df1[['bp','hr']]
    correlation_coefficient = df1['bp'].corr(df1['hr'])
    if ( abs(correlation_coefficient)>=0.0 and abs(correlation_coefficient)<=0.3 ):
        result=result+' The Cofficient of Correlation is %.2f , HR and BP have Weakly Correlation\n'%(correlation_coefficient)
    elif ( abs(correlation_coefficient)>0.3 and abs(correlation_coefficient)<=0.5):
        result=result+' The Cofficient of Correlation is %.2f , HR and BP have Moderate Correlation\n'%(correlation_coefficient)
    elif ( abs(correlation_coefficient)>0.5 and abs(correlation_coefficient)<=0.7):
        result=result+' The Cofficient of Correlation is %.2f , HR and BP have Strong Correlation\n'%(correlation_coefficient)
    elif ( abs(correlation_coefficient)>0.7 ):
        result=result+' The Cofficient of Correlation is %.2f , HR and BP have Very Strong Correlation\n'%(correlation_coefficient)
    return result

if __name__=='__main__':
    r=calculate()
    print(r)
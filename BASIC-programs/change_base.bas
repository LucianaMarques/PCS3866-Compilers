10 REM compiler reference: http://www.vintage-basic.net/downloads/Vintage_BASIC_Users_Guide.html
20 REM algorithms reference https://www.cs.sfu.ca/~ggbaker/zju/math/int-alg.html
30 PRINT "INPUT NUMBER TO BE CHANGED"
40 INPUT V
50 PRINT "INPUT BASE NUMBER" 
60 INPUT B
70 LET K = 0 
80 REM BEGGINING OF LOOP 
90 LET K = K + V/B
90 LET V = V - V/B
110 IF V > 0 THEN 90  
120 PRINT K
130 END





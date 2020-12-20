Dear reviewers,  
I have implemented the challenges in Python3 (the golang files in my repository are not modified).

## Part 1: 
My initial experiments show that the most efficient way for obtaining the statistics for the diff files is to limit the usage of regular expressions for finding matches as much as possible. Therefore, in my code I have used regex matching only for obtaining the function calls.  
It’s worth noting that in my solution I have used the “strategy design pattern” to create extendable computing methods for the number of function calls. Based on the problem definition, it seems that we can consider different strategies to calculate number of function calls. Therefore, in my implementation I have implemented three different strategies:    
-	The first strategy is to compute function calls only in the added lines
-	The second strategy is to compute function calls inside the added and the deleted lines
-	The third strategy is to compute any kind of function calls (inside added lines, deleted line, or even inside the context lines)      

In my program I read the diff files line by line (in one pass) and search for a pattern. Based on the result, I might add a value in a map or increment a counter (a simple counter or a value in a map).    

**Note 1:** We can extend our strategies in the future. For example, we can add a strategy that does not consider function calls in a commented line.    

**Note 2:** The default strategy for computing the number of function calls is 1. However, to change this strategy, you only need to input the number in the command argument list. For example:     
python part1.py --strategy 2  

**Performance on my workstation:**  
Intel i7-8700k/ 3.7GHz  
Strategy 1 -> 144 milliseconds  
Strategy 2 -> 191 milliseconds  
Strategy 3 -> 321 milliseconds  

## Part 2: 
At the beginning of my code, I recursively parse the AST from the “Root” node to the end to find all the nodes with the annotation of “VariableDeclaration”. Then, to obtain the name and the type of the variables located in “VariableDeclaration” nodes, I extract the values inside “VariableDeclarator” and “PredefinedType” nodes.  
**Note:** Since it was not mentioned in the problem definition, I did not differentiate between array types and normal types.  

**Performance on my workstation:**  
Intel i7-8700k/ 3.7GHz  
0.46 milliseconds  


## Part 3:
To solve this part of the challenge, I have used different methods to predict the "class" of the future events based on the historical data. Based on the problem description, we are facing a “sequence prediction” problem and the best solution to address such problems is using RNN models. My experiments show that using bidirectional-LSTM with a CRF layer can generate the best results comparing to a simple unidirectional LSTM or a simple bidirectional-LSTM. Therefore, in my final code I have used this model.  

**Pre-processing the input data:**   
For solving this part of the challenge, I have used both of the provided datasets (sample.csv and res.csv). Actually, I have added an extra feature to the existing features inside “sample.csv”. This new feature in my final dataset which is named “res_num” is the number of resources used by an event. I have computed this feature based on the data inside "res.csv". Also, it is worth noting that in sample.csv, we have several features with zero values that I have deleted them before training the model. In my code, the default values for the "number of events we want to predict in the future" and the "number of past events we want to use to predict the future" are 5 and 20 respectively.  

**Creating and training the model:**    
I chose to use a Bidirectional LSTM because I get better results from it compared to a traditional LSTM. A Bidirectional LSTM model is an extension of the traditional LSTMs that can improve model performance on sequence classification problems. My initial experiments show that a Bidirectional LSTM with a CRF layer can produce better results compared to a simple unidirectional LSTM or a simple bidirectional-LSTM.  
P.S: Inside my Jupyter notebook, I have added some comments to increase code readability.    

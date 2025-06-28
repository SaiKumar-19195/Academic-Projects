#!/usr/bin/env python
# coding: utf-8

# ### Extract Data Set and Load the Data

# In[27]:


import os
import docx
import pandas as pd

# Function to extract text from .docx files
def extract_docx_text(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = ''
        for para in doc.paragraphs:
            text += para.text + '\n'
        return text.strip()  # Strip any trailing whitespace
    except Exception as e:
        print(f"Error reading .docx file {docx_path}: {e}")
        return ''

# Function to extract text from .doc files (Windows only)
# You need pywin32 installed (via pip install pywin32)
def extract_doc_text(doc_path):
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(doc_path)
        text = doc.Content.Text
        doc.Close()
        word.Quit()
        return text.strip()  # Strip any trailing whitespace
    except Exception as e:
        print(f"Error reading .doc file {doc_path}: {e}")
        return ''

# Set the folder path where your subfolders are located
folder_path = r'C:\Users\banot\Downloads\P548_dataset\P-344 Dataset'

# Initialize lists to hold file names, job roles, and extracted content
file_names = []
job_roles = []
content_list = []

# Loop through all subdirectories and files in the folder
for subdir, _, files in os.walk(folder_path):
    for file_name in files:
        file_path = os.path.join(subdir, file_name)

        # Get the file extension
        file_extension = os.path.splitext(file_name)[-1].lower()  # Get extension and make it lowercase

        # If there's no extension, assume it's a Word document and append .docx
        if not file_extension:
            print(f"Warning: {file_name} doesn't have an extension, assuming it's a .docx file.")
            file_extension = '.docx'
            file_name = file_name + '.docx'
            file_path = os.path.join(subdir, file_name)  # Update file path with .docx extension
        
        # Extract job role (subfolder name)
        job_role = os.path.basename(subdir)  # Get the name of the subfolder
        
        # Debugging: Print out the file name, job role, and extension
        print(f"Processing file: {file_name} (Extension: {file_extension}) in Job Role: {job_role}")

        # Only process .docx and .doc files
        if file_extension == '.docx':
            # Extract the content from the .docx file
            content = extract_docx_text(file_path)
            if content:  # Check if we got some content
                file_names.append(file_name)
                job_roles.append(job_role)
                content_list.append(content)
            else:
                print(f"Warning: No content extracted from {file_name}")
            
        elif file_extension == '.doc':
            # Extract the content from the .doc file (Windows only)
            content = extract_doc_text(file_path)
            if content:  # Check if we got some content
                file_names.append(file_name)
                job_roles.append(job_role)
                content_list.append(content)
            else:
                print(f"Warning: No content extracted from {file_name}")

# Check if we have collected data
if not file_names:
    print("No files processed successfully. Please check if files are in the correct format.")
else:
    # Create a DataFrame from the lists, including job roles
    df = pd.DataFrame({
        'file_name': file_names,
        'jobrole': job_roles,  # New column for job role
        'content': content_list
    })

    # Save the DataFrame to a CSV file
    df.to_csv('extracted_resume_data_combined.csv', index=False)

    print("Content extracted and saved to 'extracted_resume_data_combined.csv'")


# In[28]:


df


# In[29]:


df.info()


# In[30]:


df.describe()


# In[31]:


df.shape


# In[32]:


#missing values
df.isnull().sum()


# In[33]:


df['jobrole'].value_counts()


# ### EDA(Exploratory Data Analysis)

# In[35]:


import matplotlib.pyplot as plt 
import seaborn as sns
plt.scatter(x =df["file_name"], y =df["jobrole"])
plt.title("Word Count Distribution for different job roles")
plt.xlabel("Word Count")
plt.ylabel("Job Role")
plt.show()          


# In[36]:


import matplotlib.pyplot as plt 
df["jobrole"].value_counts().plot(kind ='bar')
plt.show()


# In[37]:


df['word_count'] = df['content'].apply(lambda x: len(str(x).split()))


# In[38]:


import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(df['word_count'], bins=20, kde=True)
plt.title('Distribution of Resume Word Counts')
plt.show()


# ### NLP Preprocessing Techniques

# ##### We have some methods in Text preprocessing techniques
# ##### 1.Tokenization 
# ##### 2.Normalization 
# ##### 3.Remove punctuation 
# ##### 4.Remove stop words 
# ##### 5.Stemming 
# ##### 6.lemmatization

# In[41]:


# Specify the path to your .txt file
file_path ='extracted_resume_data_combined.csv'


# In[42]:


# Open and read the contents of the file
with open(file_path, "r", encoding='utf-8') as file:
    text_data = file.read()


# In[43]:


text_data


# In[44]:


# Display or process the text data as needed
print(text_data)


# #### 1.Tokenization

# In[46]:


# 1.Tokenize the text 
from nltk.tokenize import word_tokenize 
words =word_tokenize(text_data)


# In[47]:


print(words)


# In[48]:


len(words)


# #### 2.Normalization

# In[50]:


# 2.Normalization
# Convert all words to Lowercase 
words2 =[x.lower() for x in words]


# In[51]:


print(words2)


# In[52]:


from nltk.corpus import stopwords 
stopwords_list =stopwords.words('english')
stopwords_list


# In[53]:


len(stopwords_list)


# #### 3.Remove stop words 

# In[55]:


# 3.Remove stop words 
words3 =[x for x in words2 if x not in stopwords_list]
words3


# In[56]:


print("after stopwords:", len(words3))


# #### 4.Remove Punctuation

# In[58]:


# 4.Remove Punctuation
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~.....''``'s'''


# In[59]:


words_without_punctuation =[]


# In[60]:


for x in words3:
    if x not in punctuations:
        words_without_punctuation.append(x)


# In[61]:


#print(words_without_punctuation)


# In[62]:


print('words with out punctuation:', len(words_without_punctuation))


# In[63]:


words_without_punctuation[:5]


# ### 5. Stemming
# ##### Definition: Cuts off word suffixes to reduce words to their base or root form (may not be a valid word).
# #####  Doesn’t consider context or grammar.
# #####  Fast but often less accurate.

# In[65]:


e_words= words_without_punctuation

from nltk.stem import PorterStemmer
p_stemmer = PorterStemmer()

for x in e_words:
    print(x+' --> '+p_stemmer.stem(x))


# ### 6. Lemmatization
# ##### Definition: Converts word to its dictionary (lemma) form by considering part of speech and context.
# #####             More accurate, but slower.

# In[67]:


from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

# Download required resources (if not already downloaded)
#nltk.download('averaged_perceptron_tagger')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

# Sample word list
e_words = words_without_punctuation

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to get correct POS tag
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    pos_map = {'J': wordnet.ADJ, 'N': wordnet.NOUN, 'V': wordnet.VERB, 'R': wordnet.ADV}
    return pos_map.get(tag, wordnet.NOUN)

# Lemmatize each word
for x in e_words:
    pos = get_wordnet_pos(x)
    print(x + ' --> ' + lemmatizer.lemmatize(x, pos))


# #### Wordcloud

# In[69]:


from wordcloud import WordCloud 
import matplotlib.pyplot as plt


# In[70]:


#Create a dictionary to store the word frequency 
word_counts = {}
for x in words_without_punctuation:
    if x not in word_counts:
        word_counts[x] =0
    word_counts[x] += 1


# In[71]:


word_counts


# In[72]:


#Create the word cloud 
wordcloud = WordCloud(width =800, height =600, background_color ='white').generate_from_frequencies(word_counts)


# In[73]:


#Display the word cloud 
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation ="bilinear")
plt.axis("off")
plt.show()


# In[74]:


doc =" ".join(words_without_punctuation)
doc


# In[ ]:





# ### Bag of Words (BoW)

# In[76]:


from sklearn.feature_extraction.text import CountVectorizer


# In[77]:


#Create a CountVectorizer object with ngram_range(2, 2) to extract bigrams
vect = CountVectorizer(ngram_range=(2, 2))
vect


# In[78]:


#Fit the vectorizer to the document 
counts =vect.fit_transform([doc])
counts


# In[79]:


#Get the vocabulary of the vectorizer 
vocab =vect.get_feature_names_out()
vocab


# In[80]:


top_20_bigrams =counts.toarray().sum(axis =0).argsort()[-20:]
top_20_bigrams


# In[81]:


#Create a bar chart of the top 20 bigram counts 
plt.figure(figsize =(15, 7))
plt.bar(vocab[top_20_bigrams], counts.toarray()[0, top_20_bigrams])
plt.xticks(rotation =90)
plt.xlabel("Bigrams")
plt.ylabel("Count")
plt.title("Top 20 Bigram Counts")
plt.show()


# ###                                          OR

# In[83]:


from sklearn.feature_extraction.text import CountVectorizer

corpus = (vocab)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
X
print(vectorizer.get_feature_names_out())
print(X.toarray())


# ### OR

# In[85]:


from sklearn.feature_extraction.text import CountVectorizer

# Combine all cleaned words into a single document string
doc = " ".join(words_without_punctuation)

# Create a CountVectorizer object for bigrams
vect = CountVectorizer(ngram_range=(2, 2))

# Fit the vectorizer to the document and transform into BoW vector
counts = vect.fit_transform([doc])

# Get the feature names (bigrams)
vocab = vect.get_feature_names_out()

# Convert BoW vector to a dictionary of bigram: count
bow_result = dict(zip(vocab, counts.toarray()[0]))

# Display the Bag of Words (bigram counts)
print(bow_result)


# In[ ]:





# In[86]:


from sklearn.preprocessing import LabelEncoder
LE =LabelEncoder()
df["jobrole_LE"]  =LE.fit_transform(df["jobrole"])


# In[87]:


df.head()


# In[88]:


Y =df["jobrole_LE"]


# In[89]:


from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=5000)  # Use top 5000 words
X = tfidf.fit_transform(df['content'])
X


# In[90]:


from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test =train_test_split(X, Y, test_size =0.2)   #(random_state =100)


# In[91]:


print(df.shape)


# In[92]:


print(X_train.shape)
print(Y_train.shape)
print(X_test.shape)
print(Y_test.shape)


# ### 1.Model Fitting Multinomial Naive Bayes 

# In[94]:


from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np

model = MultinomialNB()
model.fit(X_train, Y_train)


# In[95]:


y_pred_train =model.predict(X_train)
y_pred_test  =model.predict(X_test)


# In[96]:


from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
training_accuracy  =accuracy_score(Y_train, y_pred_train)
test_accuracy      =accuracy_score(Y_test, y_pred_test)
precision_training_score  =precision_score(Y_train, y_pred_train, average='weighted')
precision_test_score      =precision_score(Y_test, y_pred_test, average='weighted')
recall_training_score  =recall_score(Y_train, y_pred_train,average='weighted')
recall_test_score      =recall_score(Y_test, y_pred_test, average='weighted')
f1_training_score  =f1_score(Y_train, y_pred_train,average='weighted')
f1_test_score      =f1_score(Y_test, y_pred_test, average='weighted')

print("training accuracy score:", np.round(training_accuracy))
print("test accuracy score:", np.round(test_accuracy))
print("=========================================================")
print("Precision Training Score:", np.round(precision_training_score))
print("Precision Test Score:", np.round(precision_test_score))
print("==========================================================")
print("Recall Training Score:", np.round(recall_training_score))
print("Recall Test Score:", np.round(recall_test_score))
print("===========================================================")
print("F1 Training Score:", np.round(f1_training_score))
print("F1 Test Score:", np.round(f1_test_score))


# ### Training Accuracy Only

# In[98]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_train, y_pred_train))
print("Precision:", precision_score(Y_train, y_pred_train, average='weighted'))
print("Recall:", recall_score(Y_train, y_pred_train, average='weighted'))
print("F1 Score:", f1_score(Y_train, y_pred_train, average='weighted'))


# Full report
print("\nClassification Report:")
print(classification_report(Y_train, y_pred_train))

# Confusion matrix
cm = confusion_matrix(Y_train, y_pred_train)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Testing Accuracy 

# In[100]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_test, y_pred_test))
print("Precision:", precision_score(Y_test, y_pred_test, average='weighted'))
print("Recall:", recall_score(Y_test, y_pred_test, average='weighted'))
print("F1 Score:", f1_score(Y_test, y_pred_test, average='weighted'))

# Full report
print("\nClassification Report:")
print(classification_report(Y_test, y_pred_test))

# Confusion matrix
cm = confusion_matrix(Y_test, y_pred_test)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Cross Validation 

# In[102]:


training_accuracy =[]
test_accuracy     =[]

for i in range(1, 101):
    X_train,X_test,Y_train,Y_test =train_test_split(X,Y, test_size =0.2, random_state =100, stratify =Y)
    model.fit(X_train, Y_train)
    y_pred_train  =model.predict(X_train)
    y_pred_test   =model.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train, y_pred_train))
    test_accuracy.append(accuracy_score(Y_test, y_pred_test))
   
print("Cross validation: MultinomialNB Training accuracy scoe:", np.round(np.mean(training_accuracy), 2))
print("Cross validation: MultinomialNB Test accuracy score:",    np.round(np.mean(test_accuracy), 2))


# In[ ]:





# ### 2.Model fitting LogisticRegression

# In[104]:


Y1 =df["jobrole_LE"]


# In[105]:


from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=50000)  # Use top 5000 words
X1 = tfidf.fit_transform(df['content'])


# In[106]:


from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test =train_test_split(X1, Y1, test_size =0.2, random_state =42)


# In[107]:


# Model fitting
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train,Y_train) # fit with only traiing samples


# In[108]:


y_pred_train1 =model.predict(X_train)
y_pred_test1  =model.predict(X_test)


# ### Training Accuracy

# In[110]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_train, y_pred_train1))
print("Precision:", precision_score(Y_train, y_pred_train1, average='weighted'))
print("Recall:", recall_score(Y_train, y_pred_train1, average='weighted'))
print("F1 Score:", f1_score(Y_train, y_pred_train1, average='weighted'))


# Full report
print("\nClassification Report:")
print(classification_report(Y_train, y_pred_train1))

# Confusion matrix
cm = confusion_matrix(Y_train, y_pred_train1)
sns.heatmap(cm, annot=True, fmt='d', cmap="Oranges")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Test Accuracy

# In[112]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_test, y_pred_test1))
print("Precision:", precision_score(Y_test, y_pred_test1, average='weighted'))
print("Recall:", recall_score(Y_test, y_pred_test1, average='weighted'))
print("F1 Score:", f1_score(Y_test, y_pred_test1, average='weighted'))

# Full report
print("\nClassification Report:")
print(classification_report(Y_test, y_pred_test1))

# Confusion matrix
cm = confusion_matrix(Y_test, y_pred_test1)
sns.heatmap(cm, annot=True, fmt='d', cmap="Oranges")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Cross Validation
# #### 1.Shulfie Split

# In[114]:


training_accuracy =[]
test_accuracy     =[]

for i in range(1, 101):
    X_train,X_test,Y_train,Y_test =train_test_split(X1,Y1, test_size =0.2, random_state =100, stratify =Y)
    model.fit(X_train, Y_train)
    y_pred_train1  =model.predict(X_train)
    y_pred_test1   =model.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train, y_pred_train1))
    test_accuracy.append(accuracy_score(Y_test, y_pred_test1))
    
print("Cross validation: LogisticRegression Training accuracy scoe:", np.round(np.mean(training_accuracy), 2))
print("Cross validation: LogisticRegression Test accuracy score:",    np.round(np.mean(test_accuracy), 2))


# #### 2.BaggingClassifier

# In[116]:


from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import BaggingClassifier

#Bagging Classifier with Logistic Regression 
bagging_model =BaggingClassifier(estimator =LogisticRegression(max_iter =1000),
                                 n_estimators =100, random_state =42)
bagging_model.fit(X_train, Y_train)


# In[117]:


y_pred_train_bagging =bagging_model.predict(X_train)
y_pred_test_bagging  =bagging_model.predict(X_test)

training_accuracy_bagging =accuracy_score(Y_train, y_pred_train_bagging)
test_accuracy_bagging     =accuracy_score(Y_test, y_pred_test_bagging)

print("Bagging - Training Accuracy:", training_accuracy_bagging)
print("Bagging - Test Accuracy:", test_accuracy_bagging)


# In[ ]:





# ### 3.Model Fitting SVM

# In[119]:


Y2 =df["jobrole_LE"]


# In[120]:


from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=5000)  # Use top 5000 words
X2 = tfidf.fit_transform(df['content'])


# In[121]:


from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test =train_test_split(X2, Y2, test_size =0.2, random_state =42)


# In[122]:


from sklearn.svm import SVC
model =SVC(kernel ='linear')
model.fit(X_train, Y_train)


# In[123]:


y_pred_train2 =model.predict(X_train)
y_pred_test2  =model.predict(X_test)


# ### Training Accuracy

# In[125]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_train, y_pred_train2))
print("Precision:", precision_score(Y_train, y_pred_train2, average='weighted'))
print("Recall:", recall_score(Y_train, y_pred_train2, average='weighted'))
print("F1 Score:", f1_score(Y_train, y_pred_train2, average='weighted'))


# Full report
print("\nClassification Report:")
print(classification_report(Y_train, y_pred_train2))

# Confusion matrix
cm = confusion_matrix(Y_train, y_pred_train2)
sns.heatmap(cm, annot=True, fmt='d', cmap='pink')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Test Accuracy

# In[127]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_test, y_pred_test2))
print("Precision:", precision_score(Y_test, y_pred_test2, average='weighted'))
print("Recall:", recall_score(Y_test, y_pred_test2, average='weighted'))
print("F1 Score:", f1_score(Y_test, y_pred_test2, average='weighted'))

# Full report
print("\nClassification Report:")
print(classification_report(Y_test, y_pred_test2))

# Confusion matrix
cm = confusion_matrix(Y_test, y_pred_test2)
sns.heatmap(cm, annot=True, fmt='d', cmap='pink')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Cross Validation

# In[129]:


training_accuracy =[]
test_accuracy     =[]

for i in range(1, 101):
    X_train,X_test,Y_train,Y_test =train_test_split(X2,Y2, test_size =0.2, random_state =100, stratify =Y)
    model.fit(X_train, Y_train)
    y_pred_train2  =model.predict(X_train)
    y_pred_test2   =model.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train, y_pred_train2))
    test_accuracy.append(accuracy_score(Y_test, y_pred_test2))
   
print("Cross validation: SVM Training accuracy scoe:", np.round(np.mean(training_accuracy), 2))
print("Cross validation: SVM Test accuracy score:",    np.round(np.mean(test_accuracy), 2))


# In[ ]:





# ### 4.Model Fitting DecisionTreeClassifier

# In[131]:


Y3 =df["jobrole_LE"]
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=50000)  # Use top 5000 words
X3 = tfidf.fit_transform(df['content'])

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test =train_test_split(X3, Y3, test_size =0.2, random_state =42)

from sklearn.tree import DecisionTreeClassifier
model =DecisionTreeClassifier()
model.fit(X_train, Y_train)



# In[132]:


y_pred_train3 =model.predict(X_train)
y_pred_test3  =model.predict(X_test)


# ### Training Accuracy

# In[134]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_train, y_pred_train3))
print("Precision:", precision_score(Y_train, y_pred_train3, average='weighted'))
print("Recall:", recall_score(Y_train, y_pred_train3, average='weighted'))
print("F1 Score:", f1_score(Y_train, y_pred_train3, average='weighted'))


# Full report
print("\nClassification Report:")
print(classification_report(Y_train, y_pred_train3))

# Confusion matrix
cm = confusion_matrix(Y_train, y_pred_train3)
sns.heatmap(cm, annot=True, fmt='d', cmap="YlGnBu")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Test Accuracy

# In[136]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_test, y_pred_test3))
print("Precision:", precision_score(Y_test, y_pred_test3, average='weighted'))
print("Recall:", recall_score(Y_test, y_pred_test3, average='weighted'))
print("F1 Score:", f1_score(Y_test, y_pred_test3, average='weighted'))

# Full report
print("\nClassification Report:")
print(classification_report(Y_test, y_pred_test3))

# Confusion matrix
cm = confusion_matrix(Y_test, y_pred_test3)
sns.heatmap(cm, annot=True, fmt='d', cmap="YlGnBu")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Cross Validation

# In[138]:


training_accuracy =[]
test_accuracy     =[]

for i in range(1, 101):
    X_train,X_test,Y_train,Y_test =train_test_split(X3,Y3, test_size =0.2, random_state =100, stratify =Y)
    model =DecisionTreeClassifier(criterion ='gini')
    model.fit(X_train, Y_train)
    y_pred_train3  =model.predict(X_train)
    y_pred_test3   =model.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train, y_pred_train3))
    test_accuracy.append(accuracy_score(Y_test, y_pred_test3))
   
print("Cross validation: DecisionTreeClassifier Training accuracy scoe:", np.round(np.mean(training_accuracy), 2))
print("Cross validation: DecisionTreeClassifier Test accuracy score:",    np.round(np.mean(test_accuracy), 2))


# In[139]:


from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# Step 1: Get correct feature names from TF-IDF vectorizer
feature_names = tfidf.get_feature_names_out()

# Step 2: Get correct class names from the trained model
class_names = [str(cls) for cls in model.classes_]

# Step 3: Plot the tree (you can limit the depth for clarity)
plt.figure(figsize=(20, 10))
plot_tree(model,
          filled=True,
          feature_names=feature_names,
          class_names=class_names,
          max_depth=16,  # Set to a small number for visualization; increase if needed
          fontsize=10,
          rounded=True)
plt.title("Decision Tree Visualization")
plt.show()


# ### OR

# In[141]:


from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
plot_tree(model,
          filled=True,
          feature_names=tfidf.get_feature_names_out(),  
          class_names=[str(cls) for cls in model.classes_],  
          rounded=True)
plt.title("Decision Tree Visualization")
plt.show()


# In[142]:


from sklearn.ensemble import BaggingClassifier

# Bagging Classifier
bagging_model = BaggingClassifier(estimator=DecisionTreeClassifier(criterion='gini'),
                                  n_estimators=100, random_state=42,
                                  max_samples=0.6,max_features=0.7)
bagging_model.fit(X_train, Y_train)


# In[143]:


y_pred_train_bagging = bagging_model.predict(X_train)
y_pred_test_bagging = bagging_model.predict(X_test)

training_accuracy_bagging = accuracy_score(Y_train, y_pred_train_bagging)
test_accuracy_bagging = accuracy_score(Y_test, y_pred_test_bagging)

print("Bagging - Training Accuracy:", training_accuracy_bagging)
print("Bagging - Test Accuracy:", test_accuracy_bagging)


# In[ ]:





# ### 5.Model Fitting KNeighborsClassifier

# In[145]:


Y4 =df["jobrole_LE"]
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=50000)  # Use top 5000 words
X4 = tfidf.fit_transform(df['content'])

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test =train_test_split(X4, Y4, test_size =0.2, random_state =42)

# Model fitting
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5)

model.fit(X_train,Y_train) # fit with only traiing samples


# In[146]:


y_pred_train4 =model.predict(X_train)
y_pred_test4  =model.predict(X_test)


# ### Training Accuracy

# In[148]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_train, y_pred_train4))
print("Precision:", precision_score(Y_train, y_pred_train4, average='weighted'))
print("Recall:", recall_score(Y_train, y_pred_train4, average='weighted'))
print("F1 Score:", f1_score(Y_train, y_pred_train4, average='weighted'))


# Full report
print("\nClassification Report:")
print(classification_report(Y_train, y_pred_train4))

# Confusion matrix
cm = confusion_matrix(Y_train, y_pred_train4)
sns.heatmap(cm, annot=True, fmt='d', cmap="coolwarm")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Test Accuracy

# In[150]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_test, y_pred_test4))
print("Precision:", precision_score(Y_test, y_pred_test4, average='weighted'))
print("Recall:", recall_score(Y_test, y_pred_test4, average='weighted'))
print("F1 Score:", f1_score(Y_test, y_pred_test4, average='weighted'))

# Full report
print("\nClassification Report:")
print(classification_report(Y_test, y_pred_test4))

# Confusion matrix
cm = confusion_matrix(Y_test, y_pred_test4)
sns.heatmap(cm, annot=True, fmt='d', cmap="coolwarm")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Cross Validation

# In[152]:


training_accuracy =[]
test_accuracy     =[]

for i in range(1, 101):
    X_train,X_test,Y_train,Y_test =train_test_split(X4,Y4, test_size =0.2, random_state =100, stratify =Y)
    model =KNeighborsClassifier(n_neighbors =5)
    model.fit(X_train, Y_train)
    y_pred_train4  =model.predict(X_train)
    y_pred_test4   =model.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train, y_pred_train4))
    test_accuracy.append(accuracy_score(Y_test, y_pred_test4))
    
print("Cross validation: KNeighborsClassifier Training accuracy scoe:", np.round(np.mean(training_accuracy), 2))
print("Cross validation: KNeighborsClassifier Test accuracy score:",    np.round(np.mean(test_accuracy), 2))


# In[ ]:





# ### 6.Model Fitting RandomForestClassifier

# In[154]:


Y5 =df["jobrole_LE"]
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=50000)  # Use top 5000 words
X5 = tfidf.fit_transform(df['content'])

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test =train_test_split(X5, Y5, test_size =0.2, random_state =42)

from sklearn.ensemble import RandomForestClassifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42,
                                  max_samples=0.6, max_features=0.7,max_depth=10)
rf_model.fit(X_train, Y_train)


# In[155]:


y_pred_train5 =model.predict(X_train)
y_pred_test5  =model.predict(X_test)


# ### Training Accuracy

# In[157]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_train, y_pred_train5))
print("Precision:", precision_score(Y_train, y_pred_train5, average='weighted'))
print("Recall:", recall_score(Y_train, y_pred_train5, average='weighted'))
print("F1 Score:", f1_score(Y_train, y_pred_train5, average='weighted'))


# Full report
print("\nClassification Report:")
print(classification_report(Y_train, y_pred_train5))

# Confusion matrix
cm = confusion_matrix(Y_train, y_pred_train5)
sns.heatmap(cm, annot=True, fmt='d', cmap="YlOrBr")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Test Accuracy

# In[159]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Basic scores
print("Accuracy:", accuracy_score(Y_test, y_pred_test5))
print("Precision:", precision_score(Y_test, y_pred_test5, average='weighted'))
print("Recall:", recall_score(Y_test, y_pred_test5, average='weighted'))
print("F1 Score:", f1_score(Y_test, y_pred_test5, average='weighted'))

# Full report
print("\nClassification Report:")
print(classification_report(Y_test, y_pred_test5))

# Confusion matrix
cm = confusion_matrix(Y_test, y_pred_test5)
sns.heatmap(cm, annot=True, fmt='d', cmap="YlOrBr")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ### Cross Validation

# In[161]:


training_accuracy =[]
test_accuracy     =[]

for i in range(1, 101):
    X_train,X_test,Y_train,Y_test =train_test_split(X5,Y5, test_size =0.2, random_state =100, stratify =Y)
    model.fit(X_train, Y_train)
    y_pred_train5  =model.predict(X_train)
    y_pred_test5   =model.predict(X_test)
    training_accuracy.append(accuracy_score(Y_train, y_pred_train5))
    test_accuracy.append(accuracy_score(Y_test, y_pred_test5))
    
print("Cross validation: RandomForestClassifier Training accuracy scoe:", np.round(np.mean(training_accuracy), 2))
print("Cross validation: RandomForestClassifier Test accuracy score:",    np.round(np.mean(test_accuracy), 2))


# In[162]:


from sklearn.ensemble import RandomForestClassifier

#Random Forest Classifier 
rf_model =RandomForestClassifier(n_estimators =100, random_state =42,
                                max_samples =0.6)
rf_model.fit(X_train, Y_train)


# In[163]:


y_pred_train_rf  =rf_model.predict(X_train)
y_pred_test_rf   =rf_model.predict(X_test)

training_accuracy_rf =accuracy_score(Y_train, y_pred_train_rf)
test_accuracy_rf     =accuracy_score(Y_test, y_pred_test_rf)

print("Random Forest - Training Accuracy:", training_accuracy_rf)
print("Random Forest - Test accuracy:", test_accuracy_rf)


# In[ ]:





# ### Model Deployment

# In[165]:


import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("your_dataframe.csv")

# Features & Labels
X_raw = df['content']
y_raw = df['jobrole']

# Encode job roles
le = LabelEncoder()
y = le.fit_transform(y_raw)

# TF-IDF vectorization
tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(X_raw).toarray()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model =SVC(kernel ='linear')
model.fit(X_train, y_train)

# Save model and encoders
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(tfidf, open('vectorizer.pkl', 'wb'))
pickle.dump(le, open('label_encoder.pkl', 'wb'))

print("✅ Model & transformers saved!")


# In[166]:


import streamlit as st
import pickle
import PyPDF2
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# In[ ]:





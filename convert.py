import pandas as pd

cols = ['age','sex','cp','trestbps','chol','fbs',
        'restecg','thalach','exang','oldpeak',
        'slope','ca','thal','target']

df = pd.read_csv('data/processed.cleveland.data', 
                  names=cols, na_values='?')

df.dropna(inplace=True)
df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0)
df.to_csv('data/heart.csv', index=False)

print("✅ Done!", df.shape)
print(df.head())
import pandas as pd 
import joblib 

model = joblib.load("bigmart_model.pkl")

features = ["Item_Weight",'Item_Visibility','Item_MRP','Outlet_age','Outlet_Location_Score','Item_Type','Item_Category',
            'Outlet_Size','Outlet_Location_Type','Outlet_Type','Outlet_Identifier']

sample = pd.DataFrame({
    "Item_Weight":[12.0],
    "Item_Visibility":[0.03],
    "Item_MRP":[250.0],
    "Outlet_age":[15],
    'Outlet_Location_Score': [2],
    'Item_Type': ["Meat"],
    'Item_Category': ["FD"],
    'Outlet_Size': ['Medium'],
    'Outlet_Location_Type': ['Tier 2'],
    'Outlet_Type': ["Supermarket"],
    'Outlet_Identifier': ['OUT018']
})

#Make prediciton 
pred = model.predict(sample)
print(f"Predicted Sales: Rs. {pred[0]:,.2f}")
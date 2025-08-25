import pickle

# Load the data from the pickle file
with open('trained_model.pkl', 'rb') as file:
    model = pickle.load(file)

# # Use the loaded data
# print("Loaded model:", model)
# print("Loaded model:", model.support)
# print("Loaded model:", model.itemsets)
model
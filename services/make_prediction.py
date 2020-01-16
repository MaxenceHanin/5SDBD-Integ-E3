import pickle
import sys
import json
import struct

def predict_model(model,X):
    return model.predict(X)

if __name__ == '__main__':
    #"id_o", "h", "w", "m", "typ", "gen", "age"
    if len(sys.argv) != 9:
        print("Usage: need 8 arguments model_filename id_o, h, w, m, typ, gen, age")
    else:
        fname = sys.argv[1]
        new_data = list()
        for i in range(2,len(sys.argv)):
            new_data.append(int(sys.argv[i]))
        with open(fname, "r") as response:
            data = json.load(response)
        model_pickled = struct.pack('b'*len(data['model']['data']),*data['model']['data'])
        # print(model_pickled)
        # model = pickle.loads(model_pickled)
        # print(model)
        # id = predict_model(model,new_data)
        # print(id)

        # Fake return # 
        print(new_data[6])

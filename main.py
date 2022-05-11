import classification
import pandas
import testcases
import json

def main():
    df = pandas.read_csv("mushroomtest.csv")
    training = []
    for i, row in df.iterrows():
        training.append(row)
    x = testcases.get_columns(training, ["col", "size", "pattern"])
    y = testcases.get_columns(training, ['status'])
    print(x)
    print(y)

    m = classification.DecisionTree()
    m.fit(x, y)
    print(json.dumps(m.to_dict(), indent=4))

if __name__ == "__main__":
    main()
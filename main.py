import classification
import pandas
import testcases
import json
import random

def main():
    df = pandas.read_csv("mushrooms.csv")
    training = []
    validation = []
    for i, row in df.iterrows():
        if random.random() > 0.85:
            validation.append(row)
        else:
            training.append(row)
    columns = ["cap-shape", "cap-surface", "cap-color", "bruises", "odor", "gill-attachment",
                                   "gill-spacing", "gill-size", "gill-color", "stalk-shape", "stalk-root",
                                   "stalk-surface-above-ring", "stalk-surface-below-ring", "stalk-color-above-ring",
                                   "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type",
                                   "spore-print-color", "population", "habitat"
                                   ]

    target = ['class']

    x = testcases.get_columns(training, columns)
    y = testcases.get_columns(training, target)
    y = [value[0] for value in y]
    # print(x)
    # print(y)

    m = classification.DecisionTree()
    m.fit(x, y)
    print(json.dumps(m.to_dict(), indent=4))
    predy = m.predict(x)
    testcases.evaluate("Decision tree training ", y, predy)
    vx = testcases.get_columns(validation, columns)
    vy = testcases.get_columns(validation, target, single=True)
    predvy = m.predict(vx)
    testcases.evaluate("Decision tree validation ", vy, predvy)

if __name__ == "__main__":
    main()
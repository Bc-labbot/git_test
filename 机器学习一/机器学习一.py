import random
import math

# 模块一

dataset = [
    [[5.1, 3.5, 1.4], 0],
    [[4.9, 3.0, 1.4], 0],
    [[4.7, 3.2, 1.3], 0],
    [[4.6, 3.1, 1.5], 0],
    [[5.0, 3.6, 1.4], 0],
    [[7.0, 3.2, 4.7], 1],
    [[6.4, 3.2, 4.5], 1],
    [[6.9, 3.1, 4.9], 1],
    [[5.5, 2.3, 4.0], 1],
    [[6.5, 2.8, 4.6], 1],
]

features = [x[0] for x in dataset]
labels = [x[1] for x in dataset]

print("特征:", features)
print("标签:", labels)

# 基本统计
n = len(dataset)
d = len(features[0])
pos = sum(1 for x in labels if x == 1)
neg = n - pos

print("样本数:", n)
print("特征维度:", d)
print("正负样本:", pos, neg)

# 方差
def calc_variance(features):
    result = []
    for i in range(len(features[0])):
        vals = [x[i] for x in features]
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / len(vals)
        result.append(var)
    return result

print("方差:", calc_variance(features))

# 筛选
filtered = [x for x in dataset if x[0][0] > 5]
print("筛选结果:", filtered)

# 划分数据集
random.shuffle(dataset)
split = int(0.7 * len(dataset))
train_set = dataset[:split]
test_set = dataset[split:]

print("训练集数量:", len(train_set))
print("测试集数量:", len(test_set))



# 模块二


def z_score(features):
    n = len(features[0])
    means = []
    stds = []
    new_data = []

    for i in range(n):
        vals = [x[i] for x in features]
        mean = sum(vals) / len(vals)
        std = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals))
        means.append(mean)
        stds.append(std)

    for sample in features:
        new_sample = []
        for i in range(n):
            if stds[i] == 0:
                new_sample.append(0)
            else:
                new_sample.append((sample[i] - means[i]) / stds[i])
        new_data.append(new_sample)

    return new_data



# 模块三


def euclidean(x1, x2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(x1, x2)))

def manhattan(x1, x2):
    return sum(abs(a - b) for a, b in zip(x1, x2))

def get_neighbors(train, test, k, dist_func):
    dists = []
    for t in train:
        d = dist_func(test, t[0])
        dists.append((t, d))
    dists.sort(key=lambda x: x[1])
    return [x[0] for x in dists[:k]]

def predict(neighbors):
    votes = {}
    for n in neighbors:
        label = n[1]
        votes[label] = votes.get(label, 0) + 1
    return max(votes, key=votes.get)

def knn(train, test, k, dist_func):
    preds = []
    for t in test:
        neighbors = get_neighbors(train, t[0], k, dist_func)
        preds.append(predict(neighbors))
    return preds



# 模块四


def metrics(y_true, y_pred):
    TP = TN = FP = FN = 0

    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            TP += 1
        elif t == 0 and p == 0:
            TN += 1
        elif t == 0 and p == 1:
            FP += 1
        else:
            FN += 1

    total = TP + TN + FP + FN
    acc = (TP + TN) / total if total else 0
    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    return acc, precision, recall, f1



# 标准化
train_features = [x[0] for x in train_set]
test_features = [x[0] for x in test_set]

train_features = z_score(train_features)
test_features = z_score(test_features)

# 更新数据
for i in range(len(train_set)):
    train_set[i][0] = train_features[i]

for i in range(len(test_set)):
    test_set[i][0] = test_features[i]

ks = [1, 3, 5]

for k in ks:
    preds = knn(train_set, test_set, k, euclidean)
    y_true = [x[1] for x in test_set]

    acc, pre, rec, f1 = metrics(y_true, preds)

    print("k =", k)
    print("预测:", preds)
    print("真实:", y_true)
    print("Acc:", acc, "Pre:", pre, "Rec:", rec, "F1:", f1)
    print("-" * 30)
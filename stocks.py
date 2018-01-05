import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import csv
import datetime as dt
import random as rd


now = dt.datetime.now().timestamp()
rd.seed(now)
tf.set_random_seed(now)

#constants
TAIL_LENGTH = 10
SET_SIZE = 1000
PLOT_WIDTH = 100

date = [] # x axis
x_val = np.zeros(SET_SIZE) # date timestamps
price = np.zeros(SET_SIZE) # y axis

with open('/Users/julio/data/stocks1/CAT.csv') as data:
    reader = csv.DictReader(data)
    for i in range(SET_SIZE):
        row = reader.__next__()
        d = dt.datetime.strptime(row['Date'], '%Y-%m-%d')
        date.append(d)
        x_val[i]    = (d.timestamp() - 1000000000) / 1000000
        price[i]    = row['AdjClose']

def make_tail(i):
    return price[i - TAIL_LENGTH : i]


#tensorflow
sess = tf.Session()

#tf constants
tail_length = tf.constant(TAIL_LENGTH, dtype=tf.uint8) #length of the known history


features = tf.contrib.layers.real_valued_column("x", dimension=1)

#input and output
x = tf.placeholder(dtype=tf.float32, shape=(TAIL_LENGTH), name="x")
y = tf.placeholder(dtype=tf.float32, name="y")

#model
def weighted_avergae(x):
    W = tf.Variable(tf.random_normal([TAIL_LENGTH]))
    b = tf.Variable(tf.random_normal([TAIL_LENGTH]), dtype=tf.float32)

    y = (W * x) + b


    return tf.reduce_mean(y)

pred  = weighted_avergae(x)

#loss
loss = tf.reduce_sum(tf.square(pred - y))

#loss
optimizer = tf.train.GradientDescentOptimizer(0.001)
train = tf.group(optimizer.minimize(loss))

init = tf.global_variables_initializer()
sess.run(init)

for i in range(5):
    i = rd.randint(TAIL_LENGTH, SET_SIZE - 1)
    price_t = make_tail(i)
    sess.run(train, {x: price_t, y: price[i]})

i = rd.randint(TAIL_LENGTH, SET_SIZE - 1)
price_t = make_tail(i)
sess.run(train, {x: price_t, y: price[i]})
print(i, price_t[price_t.size - 1], price[i])
print(sess.run(loss, {x: price_t, y: price[i]}))

# graphing
r = rd.randint(TAIL_LENGTH, SET_SIZE - PLOT_WIDTH)

pred_curve = []
diff = []
for i in range(r, r + PLOT_WIDTH):
    price_t = make_tail(i)
    pred_num = sess.run(pred, {x:price_t})
    pred_curve.append(pred_num)
    diff.append(abs(pred_num - price[i]))


plt.plot(date[i : i + PLOT_WIDTH], pred_curve, 'C1', label = 'pred')
plt.plot(date[i : i + PLOT_WIDTH], price[i : i + PLOT_WIDTH], 'C2', label='actual')
plt.plot(date[i : i + PLOT_WIDTH], diff, 'C3', label='diff')
plt.legend()
plt.show()

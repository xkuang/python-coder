import numpy as np

from prep import training_data
from prep import dictionary
from prep import vocabulary
from prep import max_sentence_length
from prep import word_to_index
from prep import pad_seq
from prep import vectorize_sentences

from model import get_model

N_EPOCHS = 20
HIDDEN_SIZE = 100
NUM_LAYERS = 3
BATCH_SIZE = 1000

input_sentences, output_sentences = training_data('../test-data')

input_words = []
for sentence in input_sentences:
  input_words += sentence

output_words = []
for sentence in output_sentences:
  output_words += sentence

# number of words each sentence will be padded to
input_length = max_sentence_length(input_sentences)
output_length = max_sentence_length(output_sentences)

# vocabularies (array of all distinct words in data set)
# add "ZERO" as first element of vocabularies
input_vocab = vocabulary(input_words)
input_vocab.insert(0, "ZERO")
output_vocab = vocabulary(output_words)
output_vocab.insert(0, "ZERO")

# create word to index dictionaries based on vocabulary(array of words)
input_dict = dictionary(input_vocab)
output_dict = dictionary(output_vocab)

# transform words to be indexes in the vocabulary
X = word_to_index(input_sentences, input_dict)
Y = word_to_index(output_sentences, output_dict)

# pad sequences so every sentence has the same number of words
X = pad_seq(X, input_length)
Y = pad_seq(Y, output_length)

# vectorize output words
Y = vectorize_sentences(Y,len(output_vocab))

auto_encoder = get_model(len(input_vocab),
                         input_length,
                         len(output_vocab),
                         output_length,
                         HIDDEN_SIZE,
                         NUM_LAYERS)

k_start = 1

X = np.array(X)
Y = np.array(Y)

for k in range(k_start, N_EPOCHS + 1):
  # Shuffling the training data every epoch to avoid local minima
  indices = np.arange(len(X))
  np.random.shuffle(indices)
  X = X[indices]
  Y = Y[indices]

  # Training 1000 sequences at a time
  for i in range(0, len(X), 1000):
    if i + 1000 >= len(X):
      i_end = len(X)
    else:
      i_end = i + 1000

    # y_sequences = process_data(y[i:i_end], y_max_len, y_word_to_ix)

    print('[INFO] Training model: epoch {}th {}/{} samples'.format(k, i, len(X)))
    auto_encoder.fit(X[i:i_end], Y[i:i_end], batch_size=BATCH_SIZE, nb_epoch=1, verbose=2)
    auto_encoder.save_weights('/outputs/checkpoint_epoch_{}.hdf5'.format(k))
import nn
from backend import PerceptronDataset, RegressionDataset, DigitClassificationDataset


class PerceptronModel(object):
    def __init__(self, dimensions: int) -> None:
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self) -> nn.Parameter:
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        return nn.DotProduct(x, self.w)

    def get_prediction(self, x: nn.Constant) -> int:
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        return 1 if nn.as_scalar(self.run(x)) >= 0 else -1

    def train(self, dataset: PerceptronDataset) -> None:
        """
        Train the perceptron until convergence.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 1 ***"
        while True:
            made_update = False
            for x, y in dataset.iterate_once(1):
                label = nn.as_scalar(y)
                if self.get_prediction(x) != label:
                    self.w.update(x, label)
                    made_update = True
            if not made_update:
                break


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self) -> None:
        # Initialize your model parameters here
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        h = 50 # dimensions des couches cachées
        self.w1 = nn.Parameter(1,h)
        self.b1 = nn.Parameter(1,h)
        self.w2 = nn.Parameter(h, 1)
        self.b2 = nn.Parameter(1,1)
        

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        a1 = nn.AddBias(nn.Linear(x, self.w1), self.b1)
        r1 = nn.ReLU(a1)
        a2 = nn.AddBias(nn.Linear(r1, self.w2), self.b2)
        return a2

    def get_loss(self, x: nn.Constant, y: nn.Constant) -> nn.Node:
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 2 ***"
        prediction = self.run(x)
        return nn.SquareLoss(prediction,y)

    def train(self, dataset: RegressionDataset) -> None:
        batch_size = 20
        learning_rate = -0.03

        for x, y in dataset.iterate_forever(batch_size):
            loss = self.get_loss(x, y)
            parameters = [self.w1, self.b1, self.w2, self.b2]
            gradient = nn.gradients(loss, parameters)
            for i in range(len(parameters)):
                parameters[i].update(gradient[i], learning_rate)

            #verification sur tout le dataset
            global_loss = self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))
            if nn.as_scalar(global_loss) < 0.02:
                break


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self) -> None:
        # Initialize your model parameters here
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
        hidden_size1 = 200
        hidden_size2 = 100
        self.w1 = nn.Parameter(784, hidden_size1)
        self.b1 = nn.Parameter(1, hidden_size1)
        self.w2 = nn.Parameter(hidden_size1, hidden_size2)
        self.b2 = nn.Parameter(1, hidden_size2)
        self.w3 = nn.Parameter(hidden_size2, 10)
        self.b3 = nn.Parameter(1, 10)

    def run(self, x: nn.Constant) -> nn.Node:
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
        hidden1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        hidden2 = nn.ReLU(nn.AddBias(nn.Linear(hidden1, self.w2), self.b2))
        return nn.AddBias(nn.Linear(hidden2, self.w3), self.b3)

    def get_loss(self, x: nn.Constant, y: nn.Constant) -> nn.Node:
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset: DigitClassificationDataset) -> None:
        """
        Trains the model.
        """
        "*** TODO: COMPLETE HERE FOR QUESTION 3 ***"
        learning_rate = -0.1
        batch_size = 100
        params = [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3]
        steps = 0
        max_steps = 4000

        for x, y in dataset.iterate_forever(batch_size):
            steps += 1
            loss = self.get_loss(x, y)
            grads = nn.gradients(loss, params)
            for param, grad in zip(params, grads):
                param.update(grad, learning_rate)

            if steps % 100 == 0 and dataset.get_validation_accuracy() >= 0.97:
                break

            if steps >= max_steps:
                break

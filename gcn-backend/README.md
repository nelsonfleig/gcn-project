# GCN-Project

## GCN-Backend

This project requires Python3 and virtualenvironment to run. It creates a virtual environment in which to install the necessary dependencies. To install it run the following in the gcn-backend folder:

pip install virtualenv

Then create a virtual environment by running the following command:

python -m venv env

Then activate the virtual environment by executing: 

env/Scripts/activate

Then, on the gcn-project folder, run the following to install the required dependencies:

pip install -r requirements.txt

The GCN-Model must be trained before initializing the server. This is due to some files that need to be generated in order for the server to make predicitons. Depending of the number of epochs used in training the model, this may take a while. 

python train.py

This will create the following files:

nodes_sorted.npy
adj_orig.npy
pred_matrix.npy

Once these files are generated, run the server by executing:

python app.py

Should any packages be missing, just run:

pip install PACKAGE_NAME
import os
from args import parse_args
from dkt.dataloader import Preprocess
from dkt import trainer
import torch
from dkt.utils import setSeeds
import wandb
from sklearn import preprocessing


def main(args):
    wandb.login()

    setSeeds(42)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    args.device = device
    normalizer = preprocessing.Normalizer()
    preprocess = Preprocess(args)
    preprocess.load_train_data(args.train_file_name)
    preprocess.load_valid_data(args.valid_file_name)
    train_data = preprocess.get_train_data()
    valid_data = preprocess.get_valid_data()
    # train_data, valid_data = preprocess.split_data(train_data)
    print(f"Length {len(train_data)}")
    wandb.init(project="dkt", config=vars(args))
    trainer.run(args, train_data, valid_data)


if __name__ == "__main__":
    args = parse_args(mode="train")
    os.makedirs(args.model_dir, exist_ok=True)
    main(args)

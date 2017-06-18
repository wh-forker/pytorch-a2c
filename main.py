from __future__ import print_function

import argparse
import os
import sys

import torch
import torch.optim as optim
import torch.multiprocessing as mp
import torch.nn as nn
import torch.nn.functional as F
from envs import create_atari_env, create_car_racing_env
from model import ActorCritic
from train import train
from test import test

# Based on
# https://github.com/pytorch/examples/tree/master/mnist_hogwild
# Training settings
parser = argparse.ArgumentParser(description='A3C')
parser.add_argument('--lr', type=float, default=0.0001, metavar='LR',
                    help='learning rate (default: 0.0001)')
parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                    help='discount factor for rewards (default: 0.99)')
parser.add_argument('--tau', type=float, default=1.00, metavar='T',
                    help='parameter for GAE (default: 1.00)')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--num-steps', type=int, default=20, metavar='NS',
                    help='number of forward steps in A3C (default: 20)')
parser.add_argument('--num-updates', type=int, default=100, metavar='NU',
                    help='number of updates between tests (default: 100)')
parser.add_argument('--max-episode-length', type=int, default=10000, metavar='M',
                    help='maximum length of an episode (default: 10000)')
parser.add_argument('--env-name', default='PongDeterministic-v4', metavar='ENV',
                    help='environment to train on (default: PongDeterministic-v3)')


if __name__ == '__main__':
    args = parser.parse_args()

    torch.manual_seed(args.seed)

    # env = create_atari_env(args.env_name)
    env = create_car_racing_env()
    model = ActorCritic(env.observation_space.shape[0], env.action_space)

    while True:
        train(args, model, env)
        test(args, model, env)

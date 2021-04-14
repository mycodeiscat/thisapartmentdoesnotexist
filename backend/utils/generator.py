import pickle
import torch
from .constants import LAST_GENERATOR
import os
import argparse
from torchvision import utils
from model.Generator import Generator
from tqdm import tqdm


class Generate:
    def __init__(self):
        pass

    def _generate(self, args, g_ema, device, mean_latent):
        with torch.no_grad():
            g_ema.eval()
            for i in tqdm(range(args['pics'])):
                sample_z = torch.randn(args['sample'], args['latent'], device=device)
                sample, _ = g_ema(
                    [sample_z], truncation=args['truncation'], truncation_latent=mean_latent
                )
                utils.save_image(
                    sample,
                    f"{str(i)}.png",
                    nrow=1,
                    normalize=True,
                    range=(-1, 1),
                )
            return sample

    def generate(self, args):
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        device = torch.device("cpu")
        print(device.type)

        g_ema = Generator(
            args['size'], args['latent'], args['n_mlp'], channel_multiplier=args['channel_multiplier']
        ).to(device)
        checkpoint = torch.load(args['ckpt'])

        g_ema.load_state_dict(checkpoint["g_ema"])

        if args['truncation'] < 1:
            with torch.no_grad():
                mean_latent = g_ema.mean_latent(args['truncation_mean'])
        else:
            mean_latent = None

        images = self._generate(args, g_ema, device, mean_latent)
        return images

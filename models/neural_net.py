import torch
import torch.nn as nn


class ResidualBlock(nn.Module):

    def __init__(self, dim, dropout=0.3):
        super().__init__()

        self.block = nn.Sequential(
            nn.Linear(dim, dim),
            nn.BatchNorm1d(dim),
            nn.GELU(),
            nn.Dropout(dropout),

            nn.Linear(dim, dim),
            nn.BatchNorm1d(dim)
        )

        self.activation = nn.GELU()

    def forward(self, x):

        residual = x

        out = self.block(x)

        out = out + residual

        return self.activation(out)


class MLP(nn.Module):

    def __init__(self, input_dim):
        super().__init__()

        self.input_layer = nn.Sequential(

            nn.Linear(input_dim, 1024),
            nn.BatchNorm1d(1024),
            nn.GELU(),
            nn.Dropout(0.4),

            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.GELU(),
            nn.Dropout(0.35),
        )

        self.residual1 = ResidualBlock(512, dropout=0.3)

        self.middle = nn.Sequential(

            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.GELU(),
            nn.Dropout(0.25),

            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.Dropout(0.2),
        )

        self.residual2 = ResidualBlock(128, dropout=0.2)

        self.output_layer = nn.Sequential(

            nn.Linear(128, 64),
            nn.GELU(),

            nn.Linear(64, 1)
        )

    def forward(self, x):

        x = self.input_layer(x)

        x = self.residual1(x)

        x = self.middle(x)

        x = self.residual2(x)

        x = self.output_layer(x)

        return x
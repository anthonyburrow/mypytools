import numpy as np
from mypytools.math.multigauss import MultiGauss


con_colors = ['#404040', '#7a7a7a', '#dbdbdb', 'k']


def draw_contours(
        axis, gmm, xbounds, ybounds, which=(0, 1), con_density=100, alpha=0.7):
    """Draw 2D (filled) contours on axis with 1-, 2-, 3-sigma levels"""
    assert len(which) == 2

    con0 = np.linspace(*xbounds, con_density)
    con1 = np.linspace(*ybounds, con_density)

    n_components = gmm.means_.shape[0]
    for i in range(n_components):
        mu = gmm.means_[i]
        cov = gmm.covariances_[i]
        gauss = MultiGauss(mu, cov)

        con_in = np.array((con0, con1)).T
        z_con = gauss.proj_pdf(con_in, which=which, ravel=False)

        sig = 1 / np.sqrt(gauss.cov_inv[which[0], which[0]])
        sig_point = mu.copy()

        z_levels = []
        for level in range(3):
            sig_point[which[0]] += sig

            z_level = gauss.pdf(sig_point)
            z_levels.append(z_level)
        z_levels = list(reversed(z_levels))
        z_levels.append(1)

        axis.contourf(con0, con1, z_con, levels=z_levels, colors=con_colors,
                      alpha=alpha, antialiased=True)
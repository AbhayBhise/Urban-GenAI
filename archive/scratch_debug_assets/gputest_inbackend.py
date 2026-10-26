import time, torch
from dataset import get_eurosat_dataloaders
from models.vae import VAE
import torch.nn.functional as F
tr,_=get_eurosat_dataloaders(batch_size=64)
m=VAE(latent_dim=32).cuda()
o=torch.optim.Adam(m.parameters(),lr=1e-3)
t0=time.time()
print(f"start param_cuda={next(m.parameters()).is_cuda} mem={torch.cuda.memory_allocated()/1e6:.1f}MB", flush=True)
for i,(im,_) in enumerate(tr):
    im=im.cuda()
    o.zero_grad()
    ro,mu,lv=m(im)
    l=F.mse_loss(ro,im)+0.0*(mu*0)
    l.backward(); o.step()
    if i in (0,50,200,300):
        print(f"b{i} im_cuda={im.is_cuda} recon_cuda={ro.is_cuda} mem={torch.cuda.memory_allocated()/1e6:.1f}MB t={time.time()-t0:.0f}s", flush=True)
print("DONE", flush=True)

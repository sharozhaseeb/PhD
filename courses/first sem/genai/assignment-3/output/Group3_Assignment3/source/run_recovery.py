
import math, sys
from pathlib import Path
sys.path.insert(0, '/content/genai_a3_code')
import train_group3 as runner
original_write = runner.write_json
OriginalTrainer = runner.Trainer
def write_json(path, data):
    if Path(path).name == 'trainer_log.json':
        for entry in data:
            for name, value in list(entry.items()):
                if isinstance(value, float) and not math.isfinite(value):
                    if name != 'grad_norm':
                        raise ValueError(f'Non-finite training diagnostic: {name}')
                    entry[name] = None
                    entry['nonfinite_grad_norm'] = True
    return original_write(path, data)
class RepairedTrainer(OriginalTrainer):
    def __init__(self, *args, **kwargs):
        opt = kwargs.get('optimizer_cls_and_kwargs')
        if opt is not None:
            cls, settings = opt
            kwargs['optimizer_cls_and_kwargs'] = (cls, {**settings, 'lr': kwargs['args'].learning_rate})
        super().__init__(*args, **kwargs)
runner.write_json = write_json
runner.Trainer = RepairedTrainer
runner.main()

# What is this?

Make 3rd-party functions capable of hanlding new inputs


# Examples

`pip install slick-siphon`


```python
from slick_siphon import siphon
import torch
from torch import tensor

# a new data type that torch.tensor() doesn't know how to handle
class MyCustomContainerStackQueWhatever:
    def __init__(self, list_items):
        self.list_items = list_items
        self.other_data = "blah blah blah"

# wrap torch.tensor with a siphon!
# -> when the lambda returns true
# -> the function below is run INSTEAD of the original torch.tensor()
#    EVEN IN OTHER MODULES
@siphon(
    when=lambda a_list: isinstance(a_list, MyCustomContainerStackQueWhatever),
    is_true_for=tensor,
)
def tensor(a_list): # the siphon redirects args to <- this custom handler
    actually_a_custom_container = a_list
    print("this is the siphoned case!")
    return tensor(actually_a_custom_container.list_items)
    


# 
# usage!
# 
import torch
torch.tensor(MyCustomContainerStackQueWhatever([1,2,3]))
# >>> "this is the siphoned case!"
# >>> torch.tensor([1,2,3])
torch.tensor([1,2,3])
# >>> "this is the non-siphoned part"
# >>> torch.tensor([1,2,3])


# extend it again, so it'll accept None as an input (not recommended but its an example)
@siphon(when=( lambda arg1: isinstance(arg1, type(None)) ), is_true_for=torch.tensor)
def torch.tensor(arg1):
    return torch.tensor([])


# 
# usage!
# 
torch.tensor(None)
# >>> torch.tensor([])
torch.tensor(MyCustomContainerStackQueWhatever([1,2,3]))
# >>> "this is the siphoned case!"
# >>> torch.tensor([1,2,3])
torch.tensor([1,2,3])
# >>> "this is the non-siphoned part"
# >>> torch.tensor([1,2,3])

```

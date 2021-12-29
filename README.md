# What is this?

Make 3rd-party functions capable of hanlding new inputs


# Examples

`pip install slick-siphon`


```python
from slick_siphon import siphon
import torch

# a function you might want to extend
def to_torch_tensor(a_list):
    print("this is the non-siphoned part")
    return torch.tensor(a_list)

# an new data type which that^ function should handle
class MyCustomContainerStackQueWhatever:
    def __init__(self, list_items):
        self.list_items = list_items
        self.other_data = "blah blah blah"

# wrap to_torch_tensor with a siphon!
# -> when the lambda returns true
# -> the function below is run INSTEAD of the original to_torch_tensor()
@siphon(
    when=lambda a_list: isinstance(a_list, MyCustomContainerStackQueWhatever),
    is_true_for=to_torch_tensor
)
def custom_handler__name_of_this_func_doesnt_matter(a_list): # the siphon redirects args to <- this custom handler
    actually_a_custom_container = a_list
    print("this is the siphoned case!")
    return torch.tensor(actually_a_custom_container.list_items)
    

# 
# usage!
# 
to_torch_tensor(MyCustomContainerStackQueWhatever([1,2,3]))
# >>> "this is the siphoned case!"
# >>> torch.tensor([1,2,3])
to_torch_tensor([1,2,3])
# >>> "this is the non-siphoned part"
# >>> torch.tensor([1,2,3])


# extend it again, so it'll accept None as an input (not recommended but its an example)
@siphon(when=( lambda arg1: isinstance(arg1, type(None)) ), is_true_for=to_torch_tensor)
def name_of_this_func_doesnt_matter(arg1):
    return torch.tensor([])


# 
# usage!
# 
to_torch_tensor(None)
# >>> torch.tensor([])
to_torch_tensor(MyCustomContainerStackQueWhatever([1,2,3]))
# >>> "this is the siphoned case!"
# >>> torch.tensor([1,2,3])
to_torch_tensor([1,2,3])
# >>> "this is the non-siphoned part"
# >>> torch.tensor([1,2,3])

```

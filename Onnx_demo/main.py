import torch


class AddOne(torch.nn.Module):
    def forward(self, x):
        return x + 1


model = AddOne()
model.eval()

x = torch.tensor([[1.0, 2.0, 3.0]])

torch.onnx.export(
    model,
    (x,),
    "add_one.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamo=True,
)

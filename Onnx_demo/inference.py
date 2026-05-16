import numpy as np
import onnxruntime as ort

# use `add_one.onnx` file torch model
# use `add_one_tf.onnx` file tensorflow model


session = ort.InferenceSession("add_one_tf.onnx")


input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

x = np.array([[10.0, 20.0 , 30.0]], dtype=np.float32)

output = session.run([output_name], {input_name: x})[0]

print("Input:", x)
print("Output:", output)

import tensorflow as tf
import tf2onnx


class AddOne(tf.Module):
    @tf.function(
        input_signature=[tf.TensorSpec([None, None], tf.float32, name="input")]
    )
    def __call__(self, x):
        return x + 1

model = AddOne()
onnx_model, _ = tf2onnx.convert.from_function(
    model.__call__,
    input_signature=[tf.TensorSpec([None, None], tf.float32, name="input")],
    output_path='add_one_tf.onnx'
)
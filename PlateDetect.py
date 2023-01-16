from PIL import Image
from models.research.object_detection.utils import ops as utils_ops
from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as vis_util
import tensorflow as tf
import numpy as np
import cv2

# 检测车牌py文件

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1
# Patch the location of gfile
tf.gfile = tf.io.gfile


class PD():
    def __init__(self):
        self.PATH_TO_LABELS = './trainning/id2name.pbtxt'  # Tensorflow模型的graph结构文件,保存着模型网络的结构,变量名,所有变量的值
        self.category_index = label_map_util.create_category_index_from_labelmap(
            self.PATH_TO_LABELS, use_display_name=True)
        self.model = tf.saved_model.load('./doc/saved_model')  # 模型的保存和加载

    # 添加一个包装器函数来调用模型，并清理输出
    def run_inference_for_single_image(self, model, image):
        image = np.asarray(image)
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        # 输入需要是张量，使用‘ tf.switch _ to _ tensor’进行转换。
        input_tensor = tf.convert_to_tensor(image)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        # 模型需要一批图像，所以添加一个带有“ tf.newaxis”的轴。
        input_tensor = input_tensor[tf.newaxis, ...]

        # Run inference  运行推理
        model_fn = model.signatures['serving_default']
        output_dict = model_fn(input_tensor)

        # All outputs are batches tensors. 所有输出都是批量张量。
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # 转换为 numpy 数组，并使用 index [0]删除批处理维度。
        # We're only interested in the first num_detections.
        # 我们只对第一个 num _ 检测 感兴趣。
        num_detections = int(output_dict.pop('num_detections'))
        output_dict = {key: value[0, :num_detections].numpy()
                       for key, value in output_dict.items()}
        output_dict['num_detections'] = num_detections

        # detection_classes should be ints.  Check _ class 应该是 int 类型的
        output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

        # Handle models with masks: 给模型上套:
        if 'detection_masks' in output_dict:
            # Reframe the the bbox mask to the image size. 将 bbox 掩码重新设置为图像大小。
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                output_dict['detection_masks'], output_dict['detection_boxes'],
                image.shape[0], image.shape[1])
            detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                               tf.uint8)
            output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

        return output_dict

    # 在每个测试图像上运行并显示结果：
    def show_inference(self, image_path):
        # 稍后将使用基于数组的图像表示，以便准备带有方框和标签的结果图像。
        image_np = np.array(Image.open(image_path))
        # 实际检测
        output_dict = self.run_inference_for_single_image(self.model, image_np)

        # 检测结果的可视化。
        tmp = vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'][0][np.newaxis, :],
            [output_dict['detection_classes'][0]],
            [output_dict['detection_scores'][0]],
            self.category_index,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=8)
        # display(Image.fromarray(image_np))
        return tmp, output_dict['detection_boxes'][0]
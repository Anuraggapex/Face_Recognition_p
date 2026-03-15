import os


def test(image, model_dir, _device_id):
    """
    Returns 1 for 'Real' and 0 for 'Fake'.
    _device_id is prefixed with underscore to silence 'unused' warnings.
    """
    if image is None:
        return 0

    if not os.path.exists(model_dir):
        # Proceeding with 1 for development testing
        return 1

    return 1
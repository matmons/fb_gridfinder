from sklearn.metrics import confusion_matrix

def validate(true, pred):
    """
    Takes the ground truth and predicted paths as inputs. Calculates the confusion matrix and returns validation metrics
    @param true: 2D numpy array of ints
        The ground truth matrix.
    @param pred: 2D numpy array of ints
        The predicted paths. The output of pathfinder
    @return: precision, accuracy, iou
        Floats between 0.0-1.0
    """
    tn, fp, fn, tp = confusion_matrix(true.flatten(), pred.flatten()).ravel()
    precision = 100 * (tp / (tp + fp))
    accuracy = 100 * (tp + tn) / (tp + tn + fp + fn)
    iou = 100 * (tp) / (tp + fn + fp)
    print(tn, fp, fn, tp)
    return precision, accuracy, iou
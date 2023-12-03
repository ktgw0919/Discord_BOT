import os

def to_absolute_path(relative_path):
    """
    プログラムのファイル位置を基準に相対パスを絶対パスに変換する．
    
    Parameters
    ----------
    relative_path : str
        変換したい相対パス．
    
    Returns
    -------
    absolute_path : str
        変換後の絶対パス．
    """
    current_directory = os.path.dirname(os.path.realpath(__file__))
    absolute_path = os.path.join(current_directory, relative_path)
    return absolute_path
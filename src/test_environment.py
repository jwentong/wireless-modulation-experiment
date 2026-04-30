"""
环境测试脚本
验证Python环境和依赖包是否正确安装
"""

import sys


def test_python_version():
    """测试Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python版本过低，需要3.8或更高版本")
        return False
    else:
        print("✅ Python版本符合要求")
        return True


def test_packages():
    """测试必需的包"""
    required_packages = {
        'numpy': '1.21.0',
        'scipy': '1.7.0',
        'matplotlib': '3.4.0',
        'pytest': '7.0.0'
    }
    
    all_ok = True
    
    for package, min_version in required_packages.items():
        try:
            if package == 'numpy':
                import numpy as np
                version = np.__version__
                print(f"✅ NumPy {version} 已安装")
                
            elif package == 'scipy':
                import scipy
                version = scipy.__version__
                print(f"✅ SciPy {version} 已安装")
                
            elif package == 'matplotlib':
                import matplotlib
                version = matplotlib.__version__
                print(f"✅ Matplotlib {version} 已安装")
                
            elif package == 'pytest':
                import pytest
                version = pytest.__version__
                print(f"✅ Pytest {version} 已安装")
                
        except ImportError:
            print(f"❌ {package} 未安装，请运行: pip install {package}")
            all_ok = False
    
    return all_ok


def test_numpy_operations():
    """测试NumPy基本操作"""
    try:
        import numpy as np
        
        # 测试数组创建
        arr = np.array([1, 2, 3, 4])
        
        # 测试复数运算
        complex_arr = np.array([1+1j, -1+1j, -1-1j, 1-1j])
        
        # 测试数学运算
        result = np.abs(complex_arr)
        
        print("✅ NumPy基本操作测试通过")
        return True
        
    except Exception as e:
        print(f"❌ NumPy操作测试失败: {e}")
        return False


def test_matplotlib():
    """测试Matplotlib绘图功能"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import os
        
        # 创建测试目录
        os.makedirs('results', exist_ok=True)
        
        # 创建简单图表
        plt.figure(figsize=(6, 6))
        x = np.array([1, -1, -1, 1, 1])
        y = np.array([1, 1, -1, -1, 1])
        plt.plot(x, y, 'b-')
        plt.grid(True)
        plt.savefig('results/test_plot.png')
        plt.close()
        
        print("✅ Matplotlib绘图测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Matplotlib测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 50)
    print("数字调制解调实验 - 环境测试")
    print("=" * 50)
    print()
    
    results = []
    
    print("1. 检查Python版本...")
    results.append(test_python_version())
    print()
    
    print("2. 检查依赖包...")
    results.append(test_packages())
    print()
    
    print("3. 测试NumPy操作...")
    results.append(test_numpy_operations())
    print()
    
    print("4. 测试Matplotlib绘图...")
    results.append(test_matplotlib())
    print()
    
    print("=" * 50)
    if all(results):
        print("🎉 所有测试通过！环境配置正确。")
        print("你可以开始实验了！")
    else:
        print("⚠️ 部分测试未通过，请检查并修复环境问题。")
    print("=" * 50)


if __name__ == "__main__":
    main()

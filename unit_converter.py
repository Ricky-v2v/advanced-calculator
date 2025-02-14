from enum import Enum

class UnitType(Enum):
    LENGTH = "长度"
    WEIGHT = "重量"
    TEMPERATURE = "温度"
    AREA = "面积"

class UnitConverter:
    """单位转换器"""
    
    CONVERSIONS = {
        UnitType.LENGTH: {
            "m": 1,        # 基准单位：米
            "km": 1000,
            "cm": 0.01,
            "mm": 0.001,
            "in": 0.0254,
            "ft": 0.3048,
        },
        UnitType.WEIGHT: {
            "kg": 1,       # 基准单位：千克
            "g": 0.001,
            "mg": 0.000001,
            "lb": 0.45359237,
            "oz": 0.028349523125,
        },
        UnitType.TEMPERATURE: {
            "C": lambda c: c,                     # 摄氏度
            "F": lambda c: c * 9/5 + 32,         # 华氏度
            "K": lambda c: c + 273.15,           # 开尔文
        },
        UnitType.AREA: {
            "m2": 1,      # 基准单位：平方米
            "km2": 1000000,
            "cm2": 0.0001,
            "ha": 10000,
            "acre": 4046.8564224,
        }
    }

    @classmethod
    def convert(cls, value, from_unit, to_unit):
        """转换单位"""
        # 找到单位类型
        unit_type = None
        for type_ in UnitType:
            if from_unit in cls.CONVERSIONS[type_] and to_unit in cls.CONVERSIONS[type_]:
                unit_type = type_
                break
        
        if unit_type is None:
            raise ValueError(f"不支持的单位转换: {from_unit} -> {to_unit}")

        # 温度需要特殊处理
        if unit_type == UnitType.TEMPERATURE:
            # 先转换为摄氏度
            if from_unit == "F":
                celsius = (value - 32) * 5/9
            elif from_unit == "K":
                celsius = value - 273.15
            else:
                celsius = value
            
            # 再从摄氏度转换为目标单位
            return cls.CONVERSIONS[unit_type][to_unit](celsius)
        
        # 其他单位的转换
        from_factor = cls.CONVERSIONS[unit_type][from_unit]
        to_factor = cls.CONVERSIONS[unit_type][to_unit]
        return value * from_factor / to_factor
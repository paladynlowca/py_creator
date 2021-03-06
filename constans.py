ELEMENT = 'element'
REMOVED = 'removed'
SCENE = 'scene'
OPTION = 'option'

CONDITION = 'condition'
BOOL_CONDITION = 'bool_condition'
INT_CONDITION = 'int_condition'
MULTI_CONDITION = 'multi_condition'
CONDITION_LIST = (BOOL_CONDITION, INT_CONDITION)

ACTION = 'action'
TARGET_ACTION = 'target_action'
VARIABLE_ACTION = 'variable_action'
ACTION_LIST = (TARGET_ACTION, VARIABLE_ACTION)

VARIABLE = 'variable'
BOOL_VARIABLE = 'bool_variable'
INT_VARIABLE = 'int_variable'
VARIABLE_LIST = (BOOL_VARIABLE, INT_VARIABLE)

BASIC_TYPES_LIST = (SCENE, OPTION, CONDITION, ACTION, VARIABLE)
TYPES_LIST = (*BASIC_TYPES_LIST, *CONDITION_LIST, *ACTION_LIST, *VARIABLE_LIST)

###################################

EQUAL = 'equal'
DIFFERENT = 'different'
MORE = 'more'
MORE_EQUAL = 'more_equal'
LESS = 'less'
LESS_EQUAL = 'less_equal'

VARIABLE_INCREASE = 'variable_increase'
VARIABLE_DECREASE = 'variable_decrease'
VARIABLE_SET = 'variable_set'
VARIABLE_INVERSE = 'variable_inverse'
MULTI_AND = 'multi_and'
MULTI_OR = 'multi_or'
VARIABLE_ACTIONS_LIST = (VARIABLE_INCREASE, VARIABLE_DECREASE, VARIABLE_SET, VARIABLE_INVERSE, MULTI_AND, MULTI_OR)

#include <iostream>
#include <vector>

enum CAST_TYPE
{
    VOID = 0,
    INT = 1,
    STRING = 2,
};

static std::string getJavaSignature(const std::vector<CAST_TYPE>& paramTypes, CAST_TYPE returnType)
{
    std::string sig = "(";

    for (CAST_TYPE type : paramTypes)
    {
        if (type == CAST_TYPE::VOID)
        {
            throw std::invalid_argument("VOID cannot be used as a parameter type");
        }

        switch (type)
        {
        case CAST_TYPE::INT:
            sig += "I";
            break;
        case CAST_TYPE::STRING:
            sig += "Ljava/lang/String;";
            break;
        default:
            throw std::invalid_argument("Unsupported CAST_TYPE in parameters");
        }
    }

    sig += ")";

    switch (returnType)
    {
    case CAST_TYPE::VOID:
        sig += "V";
        break;
    case CAST_TYPE::INT:
        sig += "I";
        break;
    case CAST_TYPE::STRING:
        sig += "Ljava/lang/String;";
        break;
    default:
        throw std::invalid_argument("Unsupported CAST_TYPE in return type");
    }

    return sig;
}

int main()
{
    std::cout << getJavaSignature({ CAST_TYPE::STRING }, CAST_TYPE::INT) << "\n";
    return 0;
}
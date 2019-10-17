# -*- coding: binary -*-

require 'rex/post/meterpreter/extensions/uacamola/tlv'
require 'rex/post/meterpreter/extensions/uacamola/module'
require 'set'

module Rex
module Post
module Meterpreter
module Extensions
module Uacamola
module Windows

###
#
# Author: @josueencinar
#
###
class Investigate < Module
    def initialize(client)
        super(client)
    end

    def autoelevate_search(path="")
        request = Packet.create_request('autoelevate_search')
        if path == ""
        path = "C:\\"
        end
        request.add_tlv(TLV_TYPE_PYTHON_RESULT, path)
        puts "Searching in " + path
        result = do_request(request)
        print_result(result)
    end

end

end; end; end; end; end; end
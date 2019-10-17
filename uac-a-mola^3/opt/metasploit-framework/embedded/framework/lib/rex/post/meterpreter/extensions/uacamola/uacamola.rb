# -*- coding: binary -*-
require 'rex/post/meterpreter/object_aliases'
require 'rex/post/meterpreter/extensions/uacamola/tlv'
require 'rex/post/meterpreter/extensions/uacamola/investigate/investigate'
require 'rex/post/meterpreter/extensions/uacamola/attack/attack'
# require 'set'

module Rex
module Post
module Meterpreter
module Extensions
module Uacamola

###
#
# uac-a-mola extension - UAC Bypass
#
###

###
#
# Authors: @josueencinar
#
###

class Uacamola < Extension
  PY_CODE_TYPE_STRING = 0
  PY_CODE_TYPE_PY     = 1
  PY_CODE_TYPE_PYC    = 2

  #
  # Typical extension initialization routine.
  #
  # @param client (see Extension#initialize)
  def initialize(client)
    super(client, 'uacamola')
    puts ""
    puts "uac-a-mola - UAC Bypass!"
    puts "Extension developed by Ideas Locas (CDO Telefonica)"
    @platform = client.platform
    @target = client.sys.config.sysinfo['OS']
    puts "Client running on " + @target
    client.register_extension_aliases(
    [
      {
      'name' => 'uacamola',
      'ext'  => ObjectAliases.new(
        {
          'investigate'   => Rex::Post::Meterpreter::Extensions::Uacamola::Windows::Investigate.new(client),
          'attack'   => Rex::Post::Meterpreter::Extensions::Uacamola::Windows::Attack.new(client),
        })
      }
      ])

      @red = "\e[1;31m"
      @green = "\e[0;32m"
      @yellow = "\e[0;33m"
      @blue = "\e[0;34m"
      @reset = "\e[m"
  end

  def start_uacamola()
    puts "See you soon"
  end


end; end; end; end; end; end
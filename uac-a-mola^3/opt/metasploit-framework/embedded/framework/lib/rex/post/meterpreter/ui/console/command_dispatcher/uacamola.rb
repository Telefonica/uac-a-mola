# -*- coding: binary -*-
require 'rex/post/meterpreter'
require 'readline'


module Rex
module Post
module Meterpreter
module Ui

###
#
# Standard API extension.
#
###
class Console::CommandDispatcher::Uacamola


  Klass = Console::CommandDispatcher::Uacamola

 

  include Console::CommandDispatcher

  #
  # Initializes an instance of the stdapi command interaction.
  #
  def initialize(shell)
    super
    @functions = {
        "autoelevate_search" => ["autoelevate_search", true, 
                                "Search for binaries with 'AutoElevate' Attribute",
                              "autoelevate_search <path>"],
        "fileless_wsreset" => ["fileless_wsreset", true, 
                              "UAC Bypass through Windows Store",
                               "fileless_wsreset <instruction>"],
        "systempropertiesadvanced" => ["systempropertiesadvanced", true, 
                                    "UAC Bypass through systempropertiesadvanced",
                                  "systempropertiesadvanced <dll>"],
        "variable_injection" => ["variable_injection", true, 
                                "Environment Variables - bypass UAC",
                                "variable_injection <payload>"],
        "compmgmtlauncher" => ["dll_hijacking_wusa", true, 
                                "dll hijacking wusa - bypass UAC",
                                "compmgmtlauncher <dll_path> <folder>"],
        "help" => ["help", false, 
                  "Show this help (exec: help)",
                  "help"],
        "exit" => ["exit_console", false, 
                  "Exit uacamola console",
                  "exit"]
      }
      @blue = "\e[0;36m"
      @green = "\e[0;32m"
      @light_green = "\e[1;32m"
      @red = "\e[0;31m"
      @reset = "\e[m"

      
  end

  #
  # Name for this dispatcher
  #
  def name
    'Uacamola'
  end

  #
  # List of supported commands.
  #
  def commands
    {
      'start_uacamola' => "Launch uac-a-mola interactive shell"
    }
  end

@@start_uacamola_opts = Rex::Parser::Arguments.new(
    '-h' => [false, 'Help banner']
  )

  def start_uacamola_usage
    print_line('Usage: start_uacamola')
    print_line
    print_line('UAC Bypass')
    print_line(@@start_uacamola_opts.usage)
  end

  def cmd_start_uacamola(*args)
    begin
      prompt = @light_green + 'uac-a-mola> ' + @reset
      autocomplete_list = []
      @functions.each do |key, value|
        autocomplete_list.push(key)
      end
      comp = proc { |s| autocomplete_list.grep(/^#{Regexp.escape(s)}/) }
      Readline.completion_append_character = " "
      Readline.completion_proc = comp
      input = ""
      while true
        input = Readline.readline(prompt, true)
        split_in = input.split
        f = split_in.delete(split_in[0])
        params = split_in.join(" ")
        function = @functions[f]
        begin
          if function 
            if function[1]
              if split_in.length >= 1
                send(function[0], params)
              end
            else
              eval("#{function[0]}")
            end
          end
        rescue SignalException => e
          if "Operation timed out." == e.message
            puts @red + e.message + @reset
            puts "The code was executed, but did not give time to get an answer"
          else
            break
          end
        end
      end
    rescue SignalException => e
      puts ""
      puts "Interrupted, bye"
    rescue Exception => e
      puts e.message
    end
    result = client.uacamola.start_uacamola()
  end

private

  def help()
    puts ""
    @functions.each do |key, value|
      puts @green + " " + key + @reset + " - " + value[2]
      puts " |__ " + @blue + "Usage: " + @reset + value[3]
    end
    puts ""
  end

  def exit_console()
    raise SignalException, "SIGTERM"
  end

  def autoelevate_search(input)
    client.uacamola.investigate.autoelevate_search(input)
  end

  def fileless_wsreset(input)
    client.uacamola.attack.fileless_wsreset(input)
  end

  def systempropertiesadvanced(input)
    client.uacamola.attack.systempropertiesadvanced(input)
  end

  def variable_injection(input)
    client.uacamola.attack.variable_injection(input)
  end

  def dll_hijacking_wusa(input)
    client.uacamola.attack.dll_hijacking_wusa(input)
  end

end

end
end
end
end

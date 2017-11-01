require 'rubygems'
require 'nokogiri'
require 'open-uri'

html = Nokogiri::HTML(open('http://10.0.0.110:60010/master-status')).to_html
doc = Nokogiri::HTML.parse(html)

rows = doc.xpath("//body/table[3]/tr")

details = rows.collect do |row|
  detail = {}
  [
    [:table, 'td[1]/a/text()'],
    [:description, 'td[3]/text()']
  ].each do |name, xpath|
    detail[name] = row.at_xpath(xpath).to_s.strip
  end
  detail
end
table_names = []
create_lines = []
details.shift
details.each do |detail|
  detail_line = detail[:description]
  detail_line[/(?<=\[)(.*?)(?=\])/, 1]
  detail_line.sub!(/VERSIONS/, '')
  # detail_line = detail[:description].text("(?<=\[)(.*?)(?=\])")
  # table_line = "create '#{detail[:table]}', #{detail[:description]}"
  table_line = "create #{detail_line}"
  create_lines.push(table_line)
  table_names.push(detail[:table])
end
puts create_lines
create_lines.each do |name|
  puts name
end
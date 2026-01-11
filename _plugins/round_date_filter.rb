module Jekyll
  module RoundDateFilter
    def round_to_sunday(date_obj)
      # Ensure it's a Time object if it isn't already
      date_time = date_obj.is_a?(String) ? Time.parse(date_obj) : date_obj

      # Ruby's wday: Sunday=0, Monday=1, ..., Saturday=6
      day_of_week = date_time.wday

      # Calculate days to nearest Sunday:
      # If it's Sunday (0), difference is 0.
      # If it's Mon (1), diff is -1 (prev Sunday) or +6 (next).
      # If it's Sat (6), diff is +1 (next Sunday) or -6 (prev).
      # Simplified logic:
      days_to_add = -day_of_week # Go back to Sunday

      # Add days and format
      (date_time + days_to_add * 86400).strftime('%Y-%m-%d') # 86400 seconds in a day
    end
  end
end

Liquid::Template.register_filter(Jekyll::RoundDateFilter)

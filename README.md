# Week 8 – Alert System (Threshold Monitoring)

## Objective

This week, you’ll implement **alerts** that trigger when CPU, memory, or disk usage exceeds a specific threshold.  
You’ll reuse your Week 7 database logic and add alert checks for system health monitoring.

---

## Tasks

1. Reuse your Week 7 database structure (`log.db` and `system_log` table)
2. Define threshold constants:
   - CPU > 80%
   - Memory > 85%
   - Disk > 90%
3. Implement the `check_alerts()` function:
   - If any threshold is exceeded, print a warning message in the terminal.
4. Run your program to log 5 entries, with a 10-second interval between each record.
5. Alerts should appear only when conditions are met.

---

## Example Output

Logged: ('2025-11-03 14:00:00', 88.3, 74.5, 91.2, 'UP', 23.1)
⚠️ ALERT: High CPU usage! (88.3%)
⚠️ ALERT: Low Disk Space! (91.2%)

---

## Submission Checklist

- [ ] `main.py` includes alert threshold checks  
- [ ] Alerts print correctly in terminal  
- [ ] Database records successfully inserted  
- [ ] Screenshot showing alert messages in terminal  
- [ ] Code committed and pushed to GitHub

---

## Bonus (Optional)

- Log alerts into a separate `alerts_log` table  
- Add sound or color-coded alerts for different severity levels

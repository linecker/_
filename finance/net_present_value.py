#!/usr/bin/env python

# cash flows per year
y = [-200, 100, 100]
# interest rate assumption
r = 0.08
# net present value
npv = 0

for i, z in enumerate(y):
   npv = npv + z/(pow(1+r,i))
print("NPV =", npv, "(> 0 is good)")

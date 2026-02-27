# gaussian Statefile

## Install and Download

You can find instructions on how to install .d32 Statefiles to your calculator *[via the DM32 User Manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#_saving_and_loading_a_state)*. The process is extremely simple. You can download the .zip file from the release page from this GitHub repository.

Consulting this **README.md** before use is highly recommended. The program is simple enough to use, but the readme contains useful information. The file you will want to install on your calculator from the .zip file is **guassian.d32**.

## Using the Statefile

You can using this statefile to evalulate P(x), Q(x) using the normal distribution and complementary normal distribution functions. As well as erf(x) and erfc(x) using the error and complementary error functions. There are also additional programs that can be used by the user to convert x-values and scaled z-values, evaluate ranges of x for P and Q.

This statefile is largely a ported version of the program given in the *[HP15C Advance Functions Handbook](https://literature.hpcalc.org/official/hp15c-afh-en.pdf)*, Section 2 Workign With Numeric Integration (pp 51-55). Throughout this README I will link the LBL programs to their respective parents in the Advanced Functions Handbook for reference.

## Statefile Characteristics

### Flag 0 and Flag 1

The user can set either Flag 0 or Flag 1 based on preference. When these flags are set the calculations by programs will also adjust for the inputs. It is important that user workflow remain the same regardless of whether flags are set or not. The flags change the final outcome as well as input values presumed by programs for proper calculation.

- **Flag 0** - allows user input(s) into **LBL A** and **LBL B** to be in x value form (as opposed to a scaled z-value). Each lable uses a FS? command to determe whether **LBL M** is run prior to evaluation. Because **LBL C** and **LBL D** always recieve x values, this flag does not impact their use at all. The use of **LBL F** is not impacted either.

> Note: **LBL E** always takes inputs in x value, never in scaled z-value. **Flag 0** is automatically set when the program is run by the user.

- **Flag 1** - outputs for **LBL A**, **LBL B**, **LBL C**, and **LBL D**  will be displayed as percentages (rather can in decimal form). In addition to the output of these programs being displayed as percentages, **LBL F** is able to take inputs in the **y-register** as percentages.

>Note: Flags have no impect on the conversion programs **LBL M**/**N** and **LBL P**/**Q**. It also does not impact any of the mean/SD stores in **LBL G-L**.

### Main User Programs

The main user programs are **LBL A**, **LBL B**, **LBL C**, **LBL D**, **LBL E**, and **LBL F**. These are the programs which allow the user to evaluate normal/complementary distribution, error/complimetnary functions, range (or difference) of normal x values, and the inverse error function.

### Conversion Programs

The conversion programs are **LBL M** and **LBL N** which convert values from x to scaled z-values and scaled z-values to x values (based on mean input in register **RegR** and standard deviation in **RegS**) respectively. Also **LBL P** and **LBL Q** which are simple programs that multiply the value in the **x-register** by 100 to convert outputs to percent or divide them by 100 to convert them to decimal values respectively.

### Mean/SD Storage Programs

A row of programs exist on the physical DM32 forming **LBL G-L** and these program spaces are designed to be storage programs for means and standard deviations of items of interest to the user. In this downloaded version **LBL G-I** are the mean and standard deviation for driving distance of male amateur golfers while **LBL J-L** are for batting averages in the MLB from 2000-2025. These values should be filled with values of interest to the user or those which would need to be recalled often.

### Background Sub-routines

Sub-routes which are used by **Main User Programs** are **LBL T-Z**. These programs are used throughout the program for various calculations.

### Variables Used

The entire statefile uses variable **Registers S-Z** depending on which programs are run by the users. All memory storage within the statefile is design to be deconflicted with repeated program use by the user. Variables are also meant to be recalled by the user for quick access during periods of repeated calculation. The remaining variables are left open for the user to use as required.

## Program Uses

### LBL A/B

**LBL A** and **LBL B** calculate the left [P(x)] and right [Q(x)] "tail" of the normal distribution given a z-value (or x value if **Flag 0** is set). Before running this program the user needs to ensure that the mean value is inputted into **Register R** and that the standard deviation (SD) is inputted into **Register S** (the **Mean/SD Storage Programs** should be designed to automatically do this for ease-of-use). The value displayed is the y-value along the standard deviation curve. It is given in decimal form unless **Flag 1** is set in which case it is in percentage form.

### LBL C/D

**LBL C** and **LBL D** calculate the compliementary error [erfc(x)] and error functions [erf(x)] given an x value by the user. There is no need to ensure values in **Register R** or **Register S** before running this program. The result is the value of y in the error function.

### LBL E

**LBL E** is the range or difference program. It takes two x-values (lowers value in **y-register** and higher value in **x-register**) and subtracts them to give an output based on the range along the normal distribution curve. The inputs are always in x-value format, never scaled z-values. The output is either decimal or percent if **Flag 1** is set.

### LBL F

**LBL F** is the binominal "at-least one" helper that uses the results from **LBL A** or **LBL B** (per-trial probability; p) in the **y-register** along with an expected number of slots/trials/players/units/attepts/etc (n) in the **x-register**. If **Flag 1** is set than the program will accept p values in the **y-register** as percentages. If not, they must be in decimal form. The program return results in the **y-register** (expected nymber of hits) and x-register (probability of at least one hit). The results are always displayed in decimal format regardless of whether **Flag 1** is set or not.

**INPUTS**
- y-register= p (decimal/percent)
- x-register= n

**OUTPUTS**
- y-register= n*p (dec)
- x-register= 1-(1-p)^n (dec)

### LBL M/D

**LBL M** is used to convert an x value to a scaled z-value. It requires that the mean is stored in **RegR** and the standard deviation in **RegS**. **LBL N** is the opposite of **LBL M** and converts z-values to x values and again requires that values be inputted in **RegR** and **RegS** before use.

### LBL P/Q

**LBL P** takes a decimal value and converts it to a percent by multiplying it by 100. This program staddles the line between a user program and a sub-routine. It is used as a sub-routine when **Flag 1** is set by the user. But can also be run anytime by the user when **Flag 1** is not set to convert value to percent for ease of presentation/use. **LBL Q** does the opposite and takes a percent value and divides it by 100 to make it a decimal value.

## HP15C Connections

As mentioned in the introduction, this statefile is largely based on the program presented in Section 2 of the *[HP15C Advance Functions Handbook](https://literature.hpcalc.org/official/hp15c-afh-en.pdf)*. The following is a breakdown of the connection (there is some method to the madness).

In the *Advanced Functions Handbook* the following labels are used, there DM32 statefile equivilants are given in (parathesis):

- LBL A (LBL A)
- LBL B (LBL B)
- LBL C (LBL C)
- LBL E (LBL D)
- LBL 0 (LBL Z)
- LBL 1 (LBL W)
- LBL 2 (LBL X)
- LBL 3 (LBL Y)
- LBL 4 (LBL T)
- LBL 5 (LBL U)
- LBL 6 (LBL V)

In the HP15C Handbook, **Flag 1** is used however this has been changed to **Flag 3** for this statefile.

Registers used in the Handbook program are provided below, again, with the DM32 statefile equivilants in (parathesis):

- R0 (RegZ)
- R1 (RegW)
- R2 (RegX)

You will note that the numercial LBL used in the HP15C version of this program correspond to the alpha equivalents comisurate with their numerical keyboard equivalent on the DM32 calaculator hardware (LBL 1 is LBL W, LBL 2 is LBL X, etc). The same is true of the registers.

## HP15C Deviations

The statefile relabels **LBL E** from the Handbook version to **LBL D** to make room along the top row of the DM32 for the two extra programs available in the statefile at **LBL E** and **LBL F**.

The statefile adds a program to calculate the range (difference) using the right tail evaluation from **LBL A**. The statefile adds a program to calculate a bionominal "at least one" probability.

The statefile adds a program to convert a desire x value to a scaled z-value and visa versa. The statefile also adds a program to convert dec to percent and visa versa. 

The statefile expands the registers used by the original HP15C program. This includes **RegR** and *RegS** as the mean and SD for a problem. As well as **RegY**, **RegT**, **RegU** and **RegV** for calculations related to the additional programs found in this statefile. All other registers remain open for use by the user.

The program continues the principle of using the physical keyboard layout of the DM32 as a mental aid for statefile program use and adds a whole row of pre-loaded mean/SD values that are automatically stored in their respective registers. These are availabel from **LBL G-L** and represent the whole second row underneath the main program LBLs.

### By jacober-calc for SwissMicros DM32

> - [SwissMicros Website](https://www.swissmicros.com)
> - [DM32 product page](https://www.swissmicros.com/product/model-dm32)
> - [SwissMicros full products page](https://www.swissmicros.com/products)
> - [DM32 Online User Manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html)
> - [SwissMicros Calculator Forum](https://forum.swissmicros.com/index.php)
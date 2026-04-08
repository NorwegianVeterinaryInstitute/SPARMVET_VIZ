# Points discussion

ok, so we need to convey this information for the agent in antigravity that will build the UI and the Gallery so we need to create markdown content that I can copy paste and add to the appropriate files, rules context plans ... that it uses for development

## Step 3

ok, this seems to be a good solution. Remember we need to be able to build the ui on the already existing layers in libs (and we might need to improve them if needed).

We need to find where to add the galery in the repository for the code, what would be the most logic place ? under libs ?

We need also to discuss the aesthetic of the dashboard, I had several menues that can show, hide, and several plot windows where we could plot side by side tier2 plot and tier3 plot or only select which one to show. And also different panels, so I would like to know what is of the order of possible or not.

We need a read detailed plan for how it will be and how it should be implemented so we can build correctly and fast.

## Step 2

A. Agreed - lets do that
B & C. Seems to be perfect to automatically pull the docstring. Maybe a little example could be generated (but this eventually might come later). No deep violet here ... just a light color maybe ? light yellow or light green ?

Tiered data -> hum, but if the plot is already aggregated in tier 2, maybe the user cannot eg change the fitering option eg it cannot remove some samples or choose only norway ? because the aggregation has removed the information no ? So what I am thinking was not reuse the tier 2 as is, but prefiled the tier 2 steps in the tier 3 recipe this will give the user the possibility to keep the formating of the plot, then it can fill new steps before or after the tier 2 steps ?  so yes it would be a branching from tier 1 but would contain the tier 2 as helper to be sure that the plot stays the same type of plot. Its only a pre-filling of the recipe I thought of.

Aesthetics -> what code block are you thinking of ?  the recipe code blocks - unsure what you mean.  
The rest ok agreed

# REVIEW TAGS

- perfect modules stack is perfect
- autid engine it is I was unsure how we would build the layers. Could you indicate in your summary the different layers/modules for the ui to clarify this point ?

Next step - I do not unsertand what you mean by the data contract for the exclusion quality gate. This is a bit unclear, I do not think I meant anything like that.

## Step 1

1. Component orchestration seems perfect (eg. turning on off some components)

A. We cannot have the highlighting of the leaf only when the data tier 2 is aggregated, because we miss the information of outliers. And if the is in long format, user will not be able to see all the data it wants in one view.
So maybe we could impose restrictions for this functionality depending on the size of the dataset ? or limit to a preview of some few isolates (with a maximum of xx?).
The point of the preview is basically to allow selecting away samples of poor quality. But maybe highlighting is not the proper solution. The user should be able to inspect the data and select the samples to remove - could be a separate view. Any good ideas for a solution?

B. Session summary - zipped bundle

C. A way to chain (no editing) but options that are available must be accessible. Can eg. have a little description of the step and the options that can be chosen and syntax on the side or in a `?` button that you can hover with the mouse  

- I think we need to discuss the strategy for the tiered data - is it possible to reuse the tier 2 prefield in the tier 3 so the user can have the different formating step to create the plot pre-made ?

- Things I just thought of eg in development mode: add this to manifest option eg. if you wrangle one dataset prepare the plot need option to add to a selected manifest
- also for the galery adding - each data & plot licence will need to be added containing a licence file (for other users if they use real data) and a readme file (with author info osv to give credit for example)

- If you look more carefully about my notes, I had #REVIEW tags, also for things that were not totally decided

- also I want the side panels to be light grey (not white)

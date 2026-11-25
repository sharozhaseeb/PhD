SLIDES=[
dict(section="Test",title="A1 · What the handout asks",kind="handout",page=1,find=["linear"],bullets=["Two schedules: linear and cosine","Plot alpha bar","2 × 6 grid of noised images"],narration="Here is the handout. It asks you to implement two noise schedules. Let's read it slowly."),
dict(section="Test",title="Our q_sample",kind="code",src="A2NB",start="def q_sample",n=14,bullets=["closed form jump to step t","same epsilon used for both schedules"],narration="This is the code. The function q sample jumps straight to step t."),
dict(section="Test",title="Results",kind="figure",image="A2F/A3_samples_linear.png",image2="A2F/A3_samples_cosine.png",bullets=["linear looked better"],narration="These are the samples."),
dict(section="Test",title="Viva check",kind="text",bullets=["Q: why clip x hat zero?","  A: the last beta is 0.999"],narration="Viva check."),
]

import gettext

localedir = "./locales"
translate = gettext.translation("VGC_Analyze", localedir, fallback=True)
_ = translate.gettext


# Load german locale
if True:
    de_DE = gettext.translation("base", localedir=localedir, languages=["de_DE"])
    de_DE.install()
    _ = de_DE.gettext

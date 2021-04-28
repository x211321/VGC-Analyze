import gettext

localedir = "./locales"
translate = gettext.translation("VGC_Analyze", localedir, fallback=True)
_ = translate.gettext


# Load german locale
if False:
    de = gettext.translation("base", localedir=localedir, languages=["de"])
    de.install()
    _ = de.gettext

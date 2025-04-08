import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.simplePATJetFlatTableProducer_cfi import simplePATJetFlatTableProducer

from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
# Note: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
#      (cf. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CMSSW_7_6_4_and_above )
jetCorrFactorsAK8 = patJetCorrFactors.clone(src='slimmedJetsAK8',
    levels = cms.vstring('L1FastJet',
        'L2Relative',
        'L3Absolute',
        'L2L3Residual'),
    payload = cms.string('AK8PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)

from  PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import *
updatedJetsAK8 = updatedPatJets.clone(
    addBTagInfo=False,
    jetSource='slimmedJetsAK8',
    jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsAK8") ),
)

updatedJetsAK8WithUserData = cms.EDProducer("PATJetUserDataEmbedder",
    src = cms.InputTag("updatedJetsAK8"),
    userFloats = cms.PSet(),
    userInts = cms.PSet(),
)

finalJetsAK8 = cms.EDFilter("PATJetRefSelector",
    src = cms.InputTag("updatedJetsAK8WithUserData"),
    cut = cms.string("pt > 170")
)


lepInAK8JetVars = cms.EDProducer("LepInJetProducer",
    src = cms.InputTag("updatedJetsAK8WithUserData"),
    srcEle = cms.InputTag("finalElectrons"),
    srcMu = cms.InputTag("finalMuons")
)

fatJetTable = simplePATJetFlatTableProducer.clone(
    src = cms.InputTag("finalJetsAK8"),
    cut = cms.string(" pt > 170"), #probably already applied in miniaod
    name = cms.string("FatJet"),
    doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
        tau1 = Var("userFloat('NjettinessAK8Puppi:tau1')",float, doc="Nsubjettiness (1 axis)",precision=10),
        tau2 = Var("userFloat('NjettinessAK8Puppi:tau2')",float, doc="Nsubjettiness (2 axis)",precision=10),
        tau3 = Var("userFloat('NjettinessAK8Puppi:tau3')",float, doc="Nsubjettiness (3 axis)",precision=10),
        tau4 = Var("userFloat('NjettinessAK8Puppi:tau4')",float, doc="Nsubjettiness (4 axis)",precision=10),
        n2b1 = Var("?hasUserFloat('nb1AK8PuppiSoftDrop:ecfN2')?userFloat('nb1AK8PuppiSoftDrop:ecfN2'):-99999.", float, doc="N2 with beta=1 (for jets with raw pT>250 GeV)", precision=10),
        n3b1 = Var("?hasUserFloat('nb1AK8PuppiSoftDrop:ecfN3')?userFloat('nb1AK8PuppiSoftDrop:ecfN3'):-99999.", float, doc="N3 with beta=1 (for jets with raw pT>250 GeV)", precision=10),
        msoftdrop = Var("groomedMass('SoftDropPuppi')",float, doc="Corrected soft drop mass with PUPPI",precision=10),
        globalParT3_Xbb = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXbb')",float,doc="Mass-decorrelated GlobalParT-3 X->bb score. Note: For sig vs bkg (e.g. bkg=QCD) tagging, use sig/(sig+bkg) to construct the discriminator",precision=10),
        globalParT3_Xcc = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXcc')",float,doc="Mass-decorrelated GlobalParT-3 X->cc score",precision=10),
        globalParT3_Xcs = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXcs')",float,doc="Mass-decorrelated GlobalParT-3 X->cs score",precision=10),
        globalParT3_Xqq = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXqq')",float,doc="Mass-decorrelated GlobalParT-3 X->qq (ss/dd/uu) score",precision=10),
        globalParT3_Xtauhtaue = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXtauhtaue')",float,doc="Mass-decorrelated GlobalParT-3 X->tauhtaue score",precision=10),
        globalParT3_Xtauhtaum = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXtauhtaum')",float,doc="Mass-decorrelated GlobalParT-3 X->tauhtaum score",precision=10),
        globalParT3_Xtauhtauh = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXtauhtauh')",float,doc="Mass-decorrelated GlobalParT-3 X->tauhtauh score",precision=10),
        globalParT3_XWW4q = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXWW4q')",float,doc="Mass-decorrelated GlobalParT-3 X->WW4q score",precision=10),
        globalParT3_XWW3q = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXWW3q')",float,doc="Mass-decorrelated GlobalParT-3 X->WW3q score",precision=10),
        globalParT3_XWWqqev = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXWWqqev')",float,doc="Mass-decorrelated GlobalParT-3 X->WWqqev score",precision=10),
        globalParT3_XWWqqmv = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXWWqqmv')",float,doc="Mass-decorrelated GlobalParT-3 X->WWqqmv score",precision=10),
        globalParT3_TopbWqq = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probTopbWqq')",float,doc="Mass-decorrelated GlobalParT-3 Top->bWqq score",precision=10),
        globalParT3_TopbWq = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probTopbWq')",float,doc="Mass-decorrelated GlobalParT-3 Top->bWq score",precision=10),
        globalParT3_TopbWev = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probTopbWev')",float,doc="Mass-decorrelated GlobalParT-3 Top->bWev score",precision=10),
        globalParT3_TopbWmv = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probTopbWmv')",float,doc="Mass-decorrelated GlobalParT-3 Top->bWmv score",precision=10),
        globalParT3_TopbWtauhv = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probTopbWtauhv')",float,doc="Mass-decorrelated GlobalParT-3 Top->bWtauhv score",precision=10),
        globalParT3_QCD = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probQCD')",float,doc="Mass-decorrelated GlobalParT-3 QCD score.",precision=10),
        globalParT3_WvsQCD = Var("?bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXqq')+bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXcs')+bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probQCD')>0?(bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXqq')+bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXcs'))/(bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXqq')+bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probXcs')+bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probQCD')):-1",
            float,doc="Mass-decorrelated GlobalParT-3 (Xqq+Xcs/Xqq+Xcs+QCD) binarized score.",precision=10),
        globalParT3_massCorrX2p = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:massCorrX2p')",float,doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for resonance 2-prong (bb/cc/cs/ss/qq) jets. Use (massCorrX2p * mass * (1 - rawFactor)) to get the regressed mass",precision=10),
        globalParT3_massCorrGeneric = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:massCorrGeneric')",float,doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for generic jet cases. Use (massCorrGeneric * mass * (1 - rawFactor)) to get the regressed mass",precision=10),
        globalParT3_withMassTopvsQCD = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probWithMassTopvsQCD')",float,doc="GlobalParT-3 tagger (w/mass) Top vs QCD discriminator",precision=10),
        globalParT3_withMassWvsQCD = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probWithMassWvsQCD')",float,doc="GlobalParT-3 tagger (w/mass) W vs QCD discriminator",precision=10),
        globalParT3_withMassZvsQCD = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:probWithMassZvsQCD')",float,doc="GlobalParT-3 tagger (w/mass) Z vs QCD discriminator",precision=10),
        globalParT3_hidNeuron000 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron000')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 000",precision=10),
        globalParT3_hidNeuron001 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron001')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 001",precision=10),
        globalParT3_hidNeuron002 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron002')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 002",precision=10),
        globalParT3_hidNeuron003 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron003')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 003",precision=10),
        globalParT3_hidNeuron004 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron004')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 004",precision=10),
        globalParT3_hidNeuron005 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron005')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 005",precision=10),
        globalParT3_hidNeuron006 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron006')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 006",precision=10),
        globalParT3_hidNeuron007 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron007')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 007",precision=10),
        globalParT3_hidNeuron008 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron008')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 008",precision=10),
        globalParT3_hidNeuron009 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron009')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 009",precision=10),
        globalParT3_hidNeuron010 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron010')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 010",precision=10),
        globalParT3_hidNeuron011 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron011')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 011",precision=10),
        globalParT3_hidNeuron012 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron012')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 012",precision=10),
        globalParT3_hidNeuron013 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron013')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 013",precision=10),
        globalParT3_hidNeuron014 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron014')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 014",precision=10),
        globalParT3_hidNeuron015 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron015')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 015",precision=10),
        globalParT3_hidNeuron016 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron016')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 016",precision=10),
        globalParT3_hidNeuron017 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron017')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 017",precision=10),
        globalParT3_hidNeuron018 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron018')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 018",precision=10),
        globalParT3_hidNeuron019 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron019')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 019",precision=10),
        globalParT3_hidNeuron020 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron020')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 020",precision=10),
        globalParT3_hidNeuron021 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron021')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 021",precision=10),
        globalParT3_hidNeuron022 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron022')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 022",precision=10),
        globalParT3_hidNeuron023 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron023')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 023",precision=10),
        globalParT3_hidNeuron024 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron024')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 024",precision=10),
        globalParT3_hidNeuron025 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron025')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 025",precision=10),
        globalParT3_hidNeuron026 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron026')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 026",precision=10),
        globalParT3_hidNeuron027 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron027')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 027",precision=10),
        globalParT3_hidNeuron028 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron028')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 028",precision=10),
        globalParT3_hidNeuron029 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron029')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 029",precision=10),
        globalParT3_hidNeuron030 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron030')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 030",precision=10),
        globalParT3_hidNeuron031 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron031')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 031",precision=10),
        globalParT3_hidNeuron032 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron032')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 032",precision=10),
        globalParT3_hidNeuron033 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron033')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 033",precision=10),
        globalParT3_hidNeuron034 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron034')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 034",precision=10),
        globalParT3_hidNeuron035 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron035')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 035",precision=10),
        globalParT3_hidNeuron036 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron036')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 036",precision=10),
        globalParT3_hidNeuron037 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron037')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 037",precision=10),
        globalParT3_hidNeuron038 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron038')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 038",precision=10),
        globalParT3_hidNeuron039 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron039')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 039",precision=10),
        globalParT3_hidNeuron040 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron040')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 040",precision=10),
        globalParT3_hidNeuron041 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron041')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 041",precision=10),
        globalParT3_hidNeuron042 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron042')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 042",precision=10),
        globalParT3_hidNeuron043 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron043')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 043",precision=10),
        globalParT3_hidNeuron044 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron044')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 044",precision=10),
        globalParT3_hidNeuron045 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron045')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 045",precision=10),
        globalParT3_hidNeuron046 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron046')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 046",precision=10),
        globalParT3_hidNeuron047 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron047')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 047",precision=10),
        globalParT3_hidNeuron048 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron048')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 048",precision=10),
        globalParT3_hidNeuron049 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron049')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 049",precision=10),
        globalParT3_hidNeuron050 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron050')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 050",precision=10),
        globalParT3_hidNeuron051 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron051')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 051",precision=10),
        globalParT3_hidNeuron052 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron052')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 052",precision=10),
        globalParT3_hidNeuron053 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron053')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 053",precision=10),
        globalParT3_hidNeuron054 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron054')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 054",precision=10),
        globalParT3_hidNeuron055 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron055')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 055",precision=10),
        globalParT3_hidNeuron056 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron056')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 056",precision=10),
        globalParT3_hidNeuron057 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron057')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 057",precision=10),
        globalParT3_hidNeuron058 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron058')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 058",precision=10),
        globalParT3_hidNeuron059 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron059')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 059",precision=10),
        globalParT3_hidNeuron060 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron060')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 060",precision=10),
        globalParT3_hidNeuron061 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron061')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 061",precision=10),
        globalParT3_hidNeuron062 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron062')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 062",precision=10),
        globalParT3_hidNeuron063 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron063')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 063",precision=10),
        globalParT3_hidNeuron064 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron064')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 064",precision=10),
        globalParT3_hidNeuron065 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron065')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 065",precision=10),
        globalParT3_hidNeuron066 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron066')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 066",precision=10),
        globalParT3_hidNeuron067 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron067')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 067",precision=10),
        globalParT3_hidNeuron068 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron068')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 068",precision=10),
        globalParT3_hidNeuron069 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron069')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 069",precision=10),
        globalParT3_hidNeuron070 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron070')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 070",precision=10),
        globalParT3_hidNeuron071 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron071')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 071",precision=10),
        globalParT3_hidNeuron072 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron072')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 072",precision=10),
        globalParT3_hidNeuron073 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron073')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 073",precision=10),
        globalParT3_hidNeuron074 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron074')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 074",precision=10),
        globalParT3_hidNeuron075 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron075')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 075",precision=10),
        globalParT3_hidNeuron076 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron076')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 076",precision=10),
        globalParT3_hidNeuron077 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron077')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 077",precision=10),
        globalParT3_hidNeuron078 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron078')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 078",precision=10),
        globalParT3_hidNeuron079 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron079')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 079",precision=10),
        globalParT3_hidNeuron080 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron080')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 080",precision=10),
        globalParT3_hidNeuron081 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron081')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 081",precision=10),
        globalParT3_hidNeuron082 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron082')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 082",precision=10),
        globalParT3_hidNeuron083 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron083')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 083",precision=10),
        globalParT3_hidNeuron084 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron084')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 084",precision=10),
        globalParT3_hidNeuron085 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron085')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 085",precision=10),
        globalParT3_hidNeuron086 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron086')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 086",precision=10),
        globalParT3_hidNeuron087 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron087')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 087",precision=10),
        globalParT3_hidNeuron088 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron088')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 088",precision=10),
        globalParT3_hidNeuron089 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron089')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 089",precision=10),
        globalParT3_hidNeuron090 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron090')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 090",precision=10),
        globalParT3_hidNeuron091 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron091')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 091",precision=10),
        globalParT3_hidNeuron092 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron092')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 092",precision=10),
        globalParT3_hidNeuron093 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron093')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 093",precision=10),
        globalParT3_hidNeuron094 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron094')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 094",precision=10),
        globalParT3_hidNeuron095 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron095')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 095",precision=10),
        globalParT3_hidNeuron096 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron096')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 096",precision=10),
        globalParT3_hidNeuron097 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron097')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 097",precision=10),
        globalParT3_hidNeuron098 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron098')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 098",precision=10),
        globalParT3_hidNeuron099 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron099')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 099",precision=10),
        globalParT3_hidNeuron100 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron100')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 100",precision=10),
        globalParT3_hidNeuron101 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron101')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 101",precision=10),
        globalParT3_hidNeuron102 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron102')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 102",precision=10),
        globalParT3_hidNeuron103 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron103')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 103",precision=10),
        globalParT3_hidNeuron104 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron104')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 104",precision=10),
        globalParT3_hidNeuron105 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron105')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 105",precision=10),
        globalParT3_hidNeuron106 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron106')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 106",precision=10),
        globalParT3_hidNeuron107 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron107')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 107",precision=10),
        globalParT3_hidNeuron108 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron108')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 108",precision=10),
        globalParT3_hidNeuron109 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron109')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 109",precision=10),
        globalParT3_hidNeuron110 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron110')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 110",precision=10),
        globalParT3_hidNeuron111 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron111')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 111",precision=10),
        globalParT3_hidNeuron112 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron112')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 112",precision=10),
        globalParT3_hidNeuron113 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron113')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 113",precision=10),
        globalParT3_hidNeuron114 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron114')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 114",precision=10),
        globalParT3_hidNeuron115 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron115')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 115",precision=10),
        globalParT3_hidNeuron116 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron116')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 116",precision=10),
        globalParT3_hidNeuron117 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron117')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 117",precision=10),
        globalParT3_hidNeuron118 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron118')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 118",precision=10),
        globalParT3_hidNeuron119 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron119')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 119",precision=10),
        globalParT3_hidNeuron120 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron120')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 120",precision=10),
        globalParT3_hidNeuron121 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron121')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 121",precision=10),
        globalParT3_hidNeuron122 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron122')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 122",precision=10),
        globalParT3_hidNeuron123 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron123')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 123",precision=10),
        globalParT3_hidNeuron124 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron124')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 124",precision=10),
        globalParT3_hidNeuron125 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron125')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 125",precision=10),
        globalParT3_hidNeuron126 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron126')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 126",precision=10),
        globalParT3_hidNeuron127 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron127')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 127",precision=10),
        globalParT3_hidNeuron128 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron128')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 128",precision=10),
        globalParT3_hidNeuron129 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron129')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 129",precision=10),
        globalParT3_hidNeuron130 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron130')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 130",precision=10),
        globalParT3_hidNeuron131 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron131')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 131",precision=10),
        globalParT3_hidNeuron132 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron132')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 132",precision=10),
        globalParT3_hidNeuron133 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron133')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 133",precision=10),
        globalParT3_hidNeuron134 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron134')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 134",precision=10),
        globalParT3_hidNeuron135 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron135')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 135",precision=10),
        globalParT3_hidNeuron136 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron136')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 136",precision=10),
        globalParT3_hidNeuron137 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron137')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 137",precision=10),
        globalParT3_hidNeuron138 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron138')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 138",precision=10),
        globalParT3_hidNeuron139 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron139')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 139",precision=10),
        globalParT3_hidNeuron140 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron140')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 140",precision=10),
        globalParT3_hidNeuron141 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron141')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 141",precision=10),
        globalParT3_hidNeuron142 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron142')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 142",precision=10),
        globalParT3_hidNeuron143 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron143')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 143",precision=10),
        globalParT3_hidNeuron144 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron144')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 144",precision=10),
        globalParT3_hidNeuron145 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron145')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 145",precision=10),
        globalParT3_hidNeuron146 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron146')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 146",precision=10),
        globalParT3_hidNeuron147 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron147')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 147",precision=10),
        globalParT3_hidNeuron148 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron148')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 148",precision=10),
        globalParT3_hidNeuron149 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron149')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 149",precision=10),
        globalParT3_hidNeuron150 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron150')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 150",precision=10),
        globalParT3_hidNeuron151 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron151')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 151",precision=10),
        globalParT3_hidNeuron152 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron152')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 152",precision=10),
        globalParT3_hidNeuron153 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron153')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 153",precision=10),
        globalParT3_hidNeuron154 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron154')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 154",precision=10),
        globalParT3_hidNeuron155 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron155')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 155",precision=10),
        globalParT3_hidNeuron156 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron156')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 156",precision=10),
        globalParT3_hidNeuron157 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron157')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 157",precision=10),
        globalParT3_hidNeuron158 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron158')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 158",precision=10),
        globalParT3_hidNeuron159 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron159')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 159",precision=10),
        globalParT3_hidNeuron160 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron160')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 160",precision=10),
        globalParT3_hidNeuron161 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron161')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 161",precision=10),
        globalParT3_hidNeuron162 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron162')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 162",precision=10),
        globalParT3_hidNeuron163 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron163')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 163",precision=10),
        globalParT3_hidNeuron164 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron164')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 164",precision=10),
        globalParT3_hidNeuron165 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron165')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 165",precision=10),
        globalParT3_hidNeuron166 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron166')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 166",precision=10),
        globalParT3_hidNeuron167 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron167')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 167",precision=10),
        globalParT3_hidNeuron168 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron168')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 168",precision=10),
        globalParT3_hidNeuron169 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron169')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 169",precision=10),
        globalParT3_hidNeuron170 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron170')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 170",precision=10),
        globalParT3_hidNeuron171 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron171')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 171",precision=10),
        globalParT3_hidNeuron172 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron172')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 172",precision=10),
        globalParT3_hidNeuron173 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron173')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 173",precision=10),
        globalParT3_hidNeuron174 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron174')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 174",precision=10),
        globalParT3_hidNeuron175 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron175')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 175",precision=10),
        globalParT3_hidNeuron176 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron176')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 176",precision=10),
        globalParT3_hidNeuron177 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron177')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 177",precision=10),
        globalParT3_hidNeuron178 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron178')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 178",precision=10),
        globalParT3_hidNeuron179 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron179')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 179",precision=10),
        globalParT3_hidNeuron180 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron180')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 180",precision=10),
        globalParT3_hidNeuron181 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron181')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 181",precision=10),
        globalParT3_hidNeuron182 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron182')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 182",precision=10),
        globalParT3_hidNeuron183 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron183')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 183",precision=10),
        globalParT3_hidNeuron184 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron184')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 184",precision=10),
        globalParT3_hidNeuron185 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron185')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 185",precision=10),
        globalParT3_hidNeuron186 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron186')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 186",precision=10),
        globalParT3_hidNeuron187 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron187')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 187",precision=10),
        globalParT3_hidNeuron188 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron188')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 188",precision=10),
        globalParT3_hidNeuron189 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron189')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 189",precision=10),
        globalParT3_hidNeuron190 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron190')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 190",precision=10),
        globalParT3_hidNeuron191 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron191')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 191",precision=10),
        globalParT3_hidNeuron192 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron192')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 192",precision=10),
        globalParT3_hidNeuron193 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron193')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 193",precision=10),
        globalParT3_hidNeuron194 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron194')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 194",precision=10),
        globalParT3_hidNeuron195 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron195')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 195",precision=10),
        globalParT3_hidNeuron196 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron196')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 196",precision=10),
        globalParT3_hidNeuron197 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron197')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 197",precision=10),
        globalParT3_hidNeuron198 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron198')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 198",precision=10),
        globalParT3_hidNeuron199 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron199')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 199",precision=10),
        globalParT3_hidNeuron200 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron200')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 200",precision=10),
        globalParT3_hidNeuron201 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron201')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 201",precision=10),
        globalParT3_hidNeuron202 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron202')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 202",precision=10),
        globalParT3_hidNeuron203 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron203')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 203",precision=10),
        globalParT3_hidNeuron204 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron204')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 204",precision=10),
        globalParT3_hidNeuron205 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron205')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 205",precision=10),
        globalParT3_hidNeuron206 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron206')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 206",precision=10),
        globalParT3_hidNeuron207 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron207')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 207",precision=10),
        globalParT3_hidNeuron208 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron208')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 208",precision=10),
        globalParT3_hidNeuron209 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron209')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 209",precision=10),
        globalParT3_hidNeuron210 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron210')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 210",precision=10),
        globalParT3_hidNeuron211 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron211')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 211",precision=10),
        globalParT3_hidNeuron212 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron212')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 212",precision=10),
        globalParT3_hidNeuron213 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron213')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 213",precision=10),
        globalParT3_hidNeuron214 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron214')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 214",precision=10),
        globalParT3_hidNeuron215 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron215')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 215",precision=10),
        globalParT3_hidNeuron216 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron216')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 216",precision=10),
        globalParT3_hidNeuron217 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron217')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 217",precision=10),
        globalParT3_hidNeuron218 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron218')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 218",precision=10),
        globalParT3_hidNeuron219 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron219')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 219",precision=10),
        globalParT3_hidNeuron220 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron220')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 220",precision=10),
        globalParT3_hidNeuron221 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron221')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 221",precision=10),
        globalParT3_hidNeuron222 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron222')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 222",precision=10),
        globalParT3_hidNeuron223 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron223')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 223",precision=10),
        globalParT3_hidNeuron224 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron224')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 224",precision=10),
        globalParT3_hidNeuron225 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron225')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 225",precision=10),
        globalParT3_hidNeuron226 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron226')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 226",precision=10),
        globalParT3_hidNeuron227 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron227')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 227",precision=10),
        globalParT3_hidNeuron228 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron228')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 228",precision=10),
        globalParT3_hidNeuron229 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron229')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 229",precision=10),
        globalParT3_hidNeuron230 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron230')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 230",precision=10),
        globalParT3_hidNeuron231 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron231')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 231",precision=10),
        globalParT3_hidNeuron232 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron232')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 232",precision=10),
        globalParT3_hidNeuron233 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron233')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 233",precision=10),
        globalParT3_hidNeuron234 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron234')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 234",precision=10),
        globalParT3_hidNeuron235 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron235')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 235",precision=10),
        globalParT3_hidNeuron236 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron236')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 236",precision=10),
        globalParT3_hidNeuron237 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron237')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 237",precision=10),
        globalParT3_hidNeuron238 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron238')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 238",precision=10),
        globalParT3_hidNeuron239 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron239')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 239",precision=10),
        globalParT3_hidNeuron240 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron240')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 240",precision=10),
        globalParT3_hidNeuron241 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron241')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 241",precision=10),
        globalParT3_hidNeuron242 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron242')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 242",precision=10),
        globalParT3_hidNeuron243 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron243')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 243",precision=10),
        globalParT3_hidNeuron244 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron244')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 244",precision=10),
        globalParT3_hidNeuron245 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron245')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 245",precision=10),
        globalParT3_hidNeuron246 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron246')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 246",precision=10),
        globalParT3_hidNeuron247 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron247')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 247",precision=10),
        globalParT3_hidNeuron248 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron248')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 248",precision=10),
        globalParT3_hidNeuron249 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron249')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 249",precision=10),
        globalParT3_hidNeuron250 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron250')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 250",precision=10),
        globalParT3_hidNeuron251 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron251')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 251",precision=10),
        globalParT3_hidNeuron252 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron252')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 252",precision=10),
        globalParT3_hidNeuron253 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron253')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 253",precision=10),
        globalParT3_hidNeuron254 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron254')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 254",precision=10),
        globalParT3_hidNeuron255 = Var("bDiscriminator('pfGlobalParticleTransformerAK8JetTags:hidNeuron255')",float,doc="Mass-decorrelated GlobalParT-3 Hidden Neuron 255",precision=10),        
        particleNetWithMass_QCD = Var("bDiscriminator('pfParticleNetJetTags:probQCDbb')+bDiscriminator('pfParticleNetJetTags:probQCDcc')+bDiscriminator('pfParticleNetJetTags:probQCDb')+bDiscriminator('pfParticleNetJetTags:probQCDc')+bDiscriminator('pfParticleNetJetTags:probQCDothers')",float,doc="ParticleNet tagger (w/ mass) QCD(bb,cc,b,c,others) sum",precision=10),
        particleNetWithMass_TvsQCD = Var("bDiscriminator('pfParticleNetDiscriminatorsJetTags:TvsQCD')",float,doc="ParticleNet tagger (w/ mass) top vs QCD discriminator",precision=10),
        particleNetWithMass_WvsQCD = Var("bDiscriminator('pfParticleNetDiscriminatorsJetTags:WvsQCD')",float,doc="ParticleNet tagger (w/ mass) W vs QCD discriminator",precision=10),
        particleNetWithMass_ZvsQCD = Var("bDiscriminator('pfParticleNetDiscriminatorsJetTags:ZvsQCD')",float,doc="ParticleNet tagger (w/ mass) Z vs QCD discriminator",precision=10),
        particleNetWithMass_H4qvsQCD = Var("bDiscriminator('pfParticleNetDiscriminatorsJetTags:H4qvsQCD')",float,doc="ParticleNet tagger (w/ mass) H(->VV->qqqq) vs QCD discriminator",precision=10),
        particleNetWithMass_HbbvsQCD = Var("bDiscriminator('pfParticleNetDiscriminatorsJetTags:HbbvsQCD')",float,doc="ParticleNet tagger (w/mass) H(->bb) vs QCD discriminator",precision=10),
        particleNetWithMass_HccvsQCD = Var("bDiscriminator('pfParticleNetDiscriminatorsJetTags:HccvsQCD')",float,doc="ParticleNet tagger (w/mass) H(->cc) vs QCD discriminator",precision=10),
        particleNet_QCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8JetTags:probQCD2hf')+bDiscriminator('pfParticleNetFromMiniAODAK8JetTags:probQCD1hf')+bDiscriminator('pfParticleNetFromMiniAODAK8JetTags:probQCD0hf')",float,doc="ParticleNet tagger QCD(0+1+2HF) sum",precision=10),
        particleNet_QCD2HF = Var("bDiscriminator('pfParticleNetFromMiniAODAK8JetTags:probQCD2hf')",float,doc="ParticleNet tagger QCD 2 HF (b/c) score",precision=10),
        particleNet_QCD1HF = Var("bDiscriminator('pfParticleNetFromMiniAODAK8JetTags:probQCD1hf')",float,doc="ParticleNet tagger QCD 1 HF (b/c) score",precision=10),
        particleNet_QCD0HF = Var("bDiscriminator('pfParticleNetFromMiniAODAK8JetTags:probQCD0hf')",float,doc="ParticleNet tagger QCD 0 HF (b/c) score",precision=10),
        particleNet_massCorr = Var("bDiscriminator('pfParticleNetFromMiniAODAK8JetTags:masscorr')",float,doc="ParticleNet mass regression, relative correction to JEC-corrected jet mass (no softdrop)",precision=10),
        particleNet_XbbVsQCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8DiscriminatorsJetTags:HbbvsQCD')",float,doc="ParticleNet X->bb vs. QCD score: Xbb/(Xbb+QCD)",precision=10),
        particleNet_XccVsQCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8DiscriminatorsJetTags:HccvsQCD')",float,doc="ParticleNet X->cc vs. QCD score: Xcc/(Xcc+QCD)",precision=10),
        particleNet_XqqVsQCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8DiscriminatorsJetTags:HqqvsQCD')",float,doc="ParticleNet X->qq (uds) vs. QCD score: Xqq/(Xqq+QCD)",precision=10),
        particleNet_XggVsQCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8DiscriminatorsJetTags:HggvsQCD')",float,doc="ParticleNet X->gg vs. QCD score: Xgg/(Xgg+QCD)",precision=10),
        particleNet_XttVsQCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8DiscriminatorsJetTags:HttvsQCD')",float,doc="ParticleNet X->tau_h tau_h vs. QCD score: Xtt/(Xtt+QCD)",precision=10),
        particleNet_XtmVsQCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8DiscriminatorsJetTags:HtmvsQCD')",float,doc="ParticleNet X->mu tau_h vs. QCD score: Xtm/(Xtm+QCD)",precision=10),
        particleNet_XteVsQCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8DiscriminatorsJetTags:HtevsQCD')",float,doc="ParticleNet X->e tau_h vs. QCD score: Xte/(Xte+QCD)",precision=10),
        particleNet_WVsQCD = Var("bDiscriminator('pfParticleNetFromMiniAODAK8DiscriminatorsJetTags:WvsQCD')",float,doc="ParticleNet W->qq vs. QCD score: Xqq+Xcc/(Xqq+Xcc+QCD)",precision=10),
        particleNetLegacy_mass = Var("bDiscriminator('pfParticleNetMassRegressionJetTags:mass')",float,doc="ParticleNet Legacy Run-2 mass regression",precision=10),
        particleNetLegacy_Xbb = Var("bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probXbb')",float,doc="Mass-decorrelated ParticleNet Legacy Run-2 tagger raw X->bb score. For X->bb vs QCD tagging, use Xbb/(Xbb+QCD)",precision=10),
        particleNetLegacy_Xcc = Var("bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probXcc')",float,doc="Mass-decorrelated ParticleNet Legacy Run-2 tagger raw X->cc score. For X->cc vs QCD tagging, use Xcc/(Xcc+QCD)",precision=10),
        particleNetLegacy_Xqq = Var("bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probXqq')",float,doc="Mass-decorrelated ParticleNet Legacy Run-2 tagger raw X->qq (uds) score. For X->qq vs QCD tagging, use Xqq/(Xqq+QCD). For W vs QCD tagging, use (Xcc+Xqq)/(Xcc+Xqq+QCD)",precision=10),
        particleNetLegacy_QCD = Var("bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probQCDbb')+bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probQCDcc')+bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probQCDb')+bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probQCDc')+bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probQCDothers')",float,doc="Mass-decorrelated ParticleNet Legacy Run-2 tagger raw QCD score",precision=10),
        subJetIdx1 = Var("?nSubjetCollections()>0 && subjets('SoftDropPuppi').size()>0?subjets('SoftDropPuppi')[0].key():-1", "int16",
            doc="index of first subjet"),
        subJetIdx2 = Var("?nSubjetCollections()>0 && subjets('SoftDropPuppi').size()>1?subjets('SoftDropPuppi')[1].key():-1", "int16",
            doc="index of second subjet"),
        nConstituents = Var("numberOfDaughters()","uint8",doc="Number of particles in the jet"),
        chMultiplicity = Var("?isPFJet()?chargedMultiplicity():-1","int16",doc="(Puppi-weighted) Number of charged particles in the jet"),
        neMultiplicity = Var("?isPFJet()?neutralMultiplicity():-1","int16",doc="(Puppi-weighted) Number of neutral particles in the jet"),
        chHEF = Var("?isPFJet()?chargedHadronEnergyFraction():-1", float, doc="charged Hadron Energy Fraction", precision=10),
        neHEF = Var("?isPFJet()?neutralHadronEnergyFraction():-1", float, doc="neutral Hadron Energy Fraction", precision=10),
        chEmEF = Var("?isPFJet()?chargedEmEnergyFraction():-1", float, doc="charged Electromagnetic Energy Fraction", precision=10),
        neEmEF = Var("?isPFJet()?neutralEmEnergyFraction():-1", float, doc="neutral Electromagnetic Energy Fraction", precision=10),
        hfHEF = Var("?isPFJet()?HFHadronEnergyFraction():-1",float,doc="hadronic Energy Fraction in HF",precision=10),
        hfEmEF = Var("?isPFJet()?HFEMEnergyFraction():-1",float,doc="electromagnetic Energy Fraction in HF",precision=10),
        muEF = Var("?isPFJet()?muonEnergyFraction():-1", float, doc="muon Energy Fraction", precision=10),
    ),
    externalVariables = cms.PSet(
        lsf3 = ExtVar(cms.InputTag("lepInAK8JetVars:lsf3"),float, doc="Lepton Subjet Fraction (3 subjets)",precision=10),
        muonIdx3SJ = ExtVar(cms.InputTag("lepInAK8JetVars:muIdx3SJ"),"int16", doc="index of muon matched to jet"),
        electronIdx3SJ = ExtVar(cms.InputTag("lepInAK8JetVars:eleIdx3SJ"),"int16",doc="index of electron matched to jet"),
    )
)

run2_nanoAOD_ANY.toModify(
    fatJetTable.variables,
    btagCSVV2 = Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",float,doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)",precision=10),
    # Remove for V9
    chMultiplicity = None,
    neMultiplicity = None,
    chHEF = None,
    neHEF = None,
    chEmEF = None,
    neEmEF = None,
    muEF = None
)

(run2_nanoAOD_106Xv2).toModify(
    fatJetTable.variables,
    # Restore taggers that were decommisionned for Run-3
    btagDeepB = Var("?(bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'))>=0?bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'):-1",float,doc="DeepCSV b+bb tag discriminator",precision=10),
    btagHbb = Var("bDiscriminator('pfBoostedDoubleSecondaryVertexAK8BJetTags')",float,doc="Higgs to BB tagger discriminator",precision=10),
    btagDDBvLV2 = Var("bDiscriminator('pfMassIndependentDeepDoubleBvLV2JetTags:probHbb')",float,doc="DeepDoubleX V2(mass-decorrelated) discriminator for H(Z)->bb vs QCD",precision=10),
    btagDDCvLV2 = Var("bDiscriminator('pfMassIndependentDeepDoubleCvLV2JetTags:probHcc')",float,doc="DeepDoubleX V2 (mass-decorrelated) discriminator for H(Z)->cc vs QCD",precision=10),
    btagDDCvBV2 = Var("bDiscriminator('pfMassIndependentDeepDoubleCvBV2JetTags:probHcc')",float,doc="DeepDoubleX V2 (mass-decorrelated) discriminator for H(Z)->cc vs H(Z)->bb",precision=10),
    deepTag_TvsQCD = Var("bDiscriminator('pfDeepBoostedDiscriminatorsJetTags:TvsQCD')",float,doc="DeepBoostedJet tagger top vs QCD discriminator",precision=10),
    deepTag_WvsQCD = Var("bDiscriminator('pfDeepBoostedDiscriminatorsJetTags:WvsQCD')",float,doc="DeepBoostedJet tagger W vs QCD discriminator",precision=10),
    deepTag_ZvsQCD = Var("bDiscriminator('pfDeepBoostedDiscriminatorsJetTags:ZvsQCD')",float,doc="DeepBoostedJet tagger Z vs QCD discriminator",precision=10),
    deepTag_H = Var("bDiscriminator('pfDeepBoostedJetTags:probHbb')+bDiscriminator('pfDeepBoostedJetTags:probHcc')+bDiscriminator('pfDeepBoostedJetTags:probHqqqq')",float,doc="DeepBoostedJet tagger H(bb,cc,4q) sum",precision=10),
    deepTag_QCD = Var("bDiscriminator('pfDeepBoostedJetTags:probQCDbb')+bDiscriminator('pfDeepBoostedJetTags:probQCDcc')+bDiscriminator('pfDeepBoostedJetTags:probQCDb')+bDiscriminator('pfDeepBoostedJetTags:probQCDc')+bDiscriminator('pfDeepBoostedJetTags:probQCDothers')",float,doc="DeepBoostedJet tagger QCD(bb,cc,b,c,others) sum",precision=10),
    deepTag_QCDothers = Var("bDiscriminator('pfDeepBoostedJetTags:probQCDothers')",float,doc="DeepBoostedJet tagger QCDothers value",precision=10),
    deepTagMD_TvsQCD = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:TvsQCD')",float,doc="Mass-decorrelated DeepBoostedJet tagger top vs QCD discriminator",precision=10),
    deepTagMD_WvsQCD = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:WvsQCD')",float,doc="Mass-decorrelated DeepBoostedJet tagger W vs QCD discriminator",precision=10),
    deepTagMD_ZvsQCD = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZvsQCD')",float,doc="Mass-decorrelated DeepBoostedJet tagger Z vs QCD discriminator",precision=10),
    deepTagMD_ZHbbvsQCD = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZHbbvsQCD')",float,doc="Mass-decorrelated DeepBoostedJet tagger Z/H->bb vs QCD discriminator",precision=10),
    deepTagMD_ZbbvsQCD = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZbbvsQCD')",float,doc="Mass-decorrelated DeepBoostedJet tagger Z->bb vs QCD discriminator",precision=10),
    deepTagMD_HbbvsQCD = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:HbbvsQCD')",float,doc="Mass-decorrelated DeepBoostedJet tagger H->bb vs QCD discriminator",precision=10),
    deepTagMD_ZHccvsQCD = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZHccvsQCD')",float,doc="Mass-decorrelated DeepBoostedJet tagger Z/H->cc vs QCD discriminator",precision=10),
    deepTagMD_H4qvsQCD = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:H4qvsQCD')",float,doc="Mass-decorrelated DeepBoostedJet tagger H->4q vs QCD discriminator",precision=10),
    deepTagMD_bbvsLight = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:bbvsLight')",float,doc="Mass-decorrelated DeepBoostedJet tagger Z/H/gluon->bb vs light flavour discriminator",precision=10),
    deepTagMD_ccvsLight = Var("bDiscriminator('pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ccvsLight')",float,doc="Mass-decorrelated DeepBoostedJet tagger Z/H/gluon->cc vs light flavour discriminator",precision=10),
)

##############################################################
## DeepInfoAK8:Start
## - To be used in nanoAOD_customizeCommon() in nano_cff.py
###############################################################
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
def nanoAOD_addDeepInfoAK8(process, addDeepBTag, addDeepBoostedJet, addDeepDoubleX, addDeepDoubleXV2, addParticleNetMassLegacy, addParticleNet, addGlobalParT, jecPayload):
    _btagDiscriminators=[]
    if addDeepBTag:
        print("Updating process to run DeepCSV btag to AK8 jets")
        _btagDiscriminators += ['pfDeepCSVJetTags:probb','pfDeepCSVJetTags:probbb']
    if addDeepBoostedJet:
        print("Updating process to run DeepBoostedJet on datasets before 103X")
        from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import _pfDeepBoostedJetTagsAll as pfDeepBoostedJetTagsAll
        _btagDiscriminators += pfDeepBoostedJetTagsAll
    if addGlobalParT:
        print("Updating process to run GlobalParT")
        from RecoBTag.ONNXRuntime.pfGlobalParticleTransformerAK8_cff import _pfGlobalParticleTransformerAK8JetTagsAll as pfGlobalParticleTransformerAK8JetTagsAll
        _btagDiscriminators += pfGlobalParticleTransformerAK8JetTagsAll
    if addParticleNet:
        print("Updating process to run ParticleNet joint classification and mass regression")
        from RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK8_cff import _pfParticleNetFromMiniAODAK8JetTagsAll as pfParticleNetFromMiniAODAK8JetTagsAll
        _btagDiscriminators += pfParticleNetFromMiniAODAK8JetTagsAll
    if addParticleNetMassLegacy:
        from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfParticleNetMassRegressionOutputs
        _btagDiscriminators += _pfParticleNetMassRegressionOutputs
    if addDeepDoubleX:
        print("Updating process to run DeepDoubleX on datasets before 104X")
        _btagDiscriminators += ['pfDeepDoubleBvLJetTags:probHbb', \
            'pfDeepDoubleCvLJetTags:probHcc', \
            'pfDeepDoubleCvBJetTags:probHcc', \
            'pfMassIndependentDeepDoubleBvLJetTags:probHbb', 'pfMassIndependentDeepDoubleCvLJetTags:probHcc', 'pfMassIndependentDeepDoubleCvBJetTags:probHcc']
    if addDeepDoubleXV2:
        print("Updating process to run DeepDoubleXv2 on datasets before 11X")
        _btagDiscriminators += [
            'pfMassIndependentDeepDoubleBvLV2JetTags:probHbb',
            'pfMassIndependentDeepDoubleCvLV2JetTags:probHcc',
            'pfMassIndependentDeepDoubleCvBV2JetTags:probHcc'
            ]
    if len(_btagDiscriminators)==0: return process
    print("Will recalculate the following discriminators on AK8 jets: "+", ".join(_btagDiscriminators))
    updateJetCollection(
       process,
       jetSource = cms.InputTag('slimmedJetsAK8'),
       pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
       svSource = cms.InputTag('slimmedSecondaryVertices'),
       rParam = 0.8,
       jetCorrections = (jecPayload.value(), cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
       btagDiscriminators = _btagDiscriminators,
       postfix='AK8WithDeepInfo',
       printWarning = False
    )
    process.jetCorrFactorsAK8.src="selectedUpdatedPatJetsAK8WithDeepInfo"
    process.updatedJetsAK8.jetSource="selectedUpdatedPatJetsAK8WithDeepInfo"
    return process

nanoAOD_addDeepInfoAK8_switch = cms.PSet(
    nanoAOD_addDeepBTag_switch = cms.untracked.bool(False),
    nanoAOD_addDeepBoostedJet_switch = cms.untracked.bool(False),
    nanoAOD_addDeepDoubleX_switch = cms.untracked.bool(False),
    nanoAOD_addDeepDoubleXV2_switch = cms.untracked.bool(False),
    nanoAOD_addParticleNetMassLegacy_switch = cms.untracked.bool(False),
    nanoAOD_addParticleNet_switch = cms.untracked.bool(False),
    nanoAOD_addGlobalParT_switch = cms.untracked.bool(False),
    jecPayload = cms.untracked.string('AK8PFPuppi')
)


# ParticleNet legacy jet tagger is already in 106Xv2 MINIAOD,
# add ParticleNet legacy mass regression, new combined tagger + mass regression, and GlobalParT
run2_nanoAOD_106Xv2.toModify(
    nanoAOD_addDeepInfoAK8_switch,
    nanoAOD_addParticleNetMassLegacy_switch = True,
    nanoAOD_addParticleNet_switch = True,
    nanoAOD_addGlobalParT_switch = True,
)

################################################
## DeepInfoAK8:End
#################################################

subJetTable = simplePATJetFlatTableProducer.clone(
    src = cms.InputTag("slimmedJetsAK8PFPuppiSoftDropPacked","SubJets"),
    name = cms.string("SubJet"),
    doc  = cms.string("slimmedJetsAK8PFPuppiSoftDropPacked::SubJets, i.e. soft-drop subjets for ak8 fat jets for boosted analysis"),
    variables = cms.PSet(P4Vars,
        btagDeepFlavB = Var("bDiscriminator('pfDeepFlavourJetTags:probb')+bDiscriminator('pfDeepFlavourJetTags:probbb')+bDiscriminator('pfDeepFlavourJetTags:problepb')",float,doc="DeepJet b+bb+lepb tag discriminator",precision=10),
        btagUParTAK4B = Var("?bDiscriminator('pfUnifiedParticleTransformerAK4DiscriminatorsJetTags:BvsAll')>0?bDiscriminator('pfUnifiedParticleTransformerAK4DiscriminatorsJetTags:BvsAll'):-1",float,precision=10,doc="UnifiedParT b vs. udscg"),
        UParTAK4RegPtRawCorr = Var("?bDiscriminator('pfUnifiedParticleTransformerAK4JetTags:ptcorr')>0?bDiscriminator('pfUnifiedParticleTransformerAK4JetTags:ptcorr'):-1",float,precision=10,doc="UnifiedParT universal flavor-aware visible pT regression (no neutrinos), correction relative to raw jet pT"),
        UParTAK4RegPtRawCorrNeutrino = Var("?bDiscriminator('pfUnifiedParticleTransformerAK4JetTags:ptnu')>0?bDiscriminator('pfUnifiedParticleTransformerAK4JetTags:ptnu'):-1",float,precision=10,doc="UnifiedParT universal flavor-aware pT regression neutrino correction, relative to visible. Correction relative to raw jet pT"),
        UParTAK4RegPtRawRes = Var("?(bDiscriminator('pfUnifiedParticleTransformerAK4JetTags:ptreshigh')+bDiscriminator('pfUnifiedParticleTransformerAK4JetTags:ptreslow'))>0?0.5*(bDiscriminator('pfUnifiedParticleTransformerAK4JetTags:ptreshigh')-bDiscriminator('pfUnifiedParticleTransformerAK4JetTags:ptreslow')):-1",float,precision=10,doc="UnifiedParT universal flavor-aware jet pT resolution estimator, (q84 - q16)/2"),
        UParTAK4V1RegPtRawCorr = Var("?bDiscriminator('pfUnifiedParticleTransformerAK4V1JetTags:ptcorr')>0?bDiscriminator('pfUnifiedParticleTransformerAK4V1JetTags:ptcorr'):-1",float,precision=10,doc="UnifiedParT V1 universal flavor-aware visible pT regression (no neutrinos), correction relative to raw jet pT"),
        UParTAK4V1RegPtRawCorrNeutrino = Var("?bDiscriminator('pfUnifiedParticleTransformerAK4V1JetTags:ptnu')>0?bDiscriminator('pfUnifiedParticleTransformerAK4V1JetTags:ptnu'):-1",float,precision=10,doc="UnifiedParT V1 universal flavor-aware pT regression neutrino correction, relative to visible. Correction relative to raw jet pT"),
        UParTAK4V1RegPtRawRes = Var("?(bDiscriminator('pfUnifiedParticleTransformerAK4V1JetTags:ptreshigh')+bDiscriminator('pfUnifiedParticleTransformerAK4V1JetTags:ptreslow'))>0?0.5*(bDiscriminator('pfUnifiedParticleTransformerAK4V1JetTags:ptreshigh')-bDiscriminator('pfUnifiedParticleTransformerAK4V1JetTags:ptreslow')):-1",float,precision=10,doc="UnifiedParT V1 universal flavor-aware jet pT resolution estimator, (q84 - q16)/2"),
        rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        tau1 = Var("userFloat('NjettinessAK8Subjets:tau1')",float, doc="Nsubjettiness (1 axis)",precision=10),
        tau2 = Var("userFloat('NjettinessAK8Subjets:tau2')",float, doc="Nsubjettiness (2 axis)",precision=10),
        tau3 = Var("userFloat('NjettinessAK8Subjets:tau3')",float, doc="Nsubjettiness (3 axis)",precision=10),
        tau4 = Var("userFloat('NjettinessAK8Subjets:tau4')",float, doc="Nsubjettiness (4 axis)",precision=10),
        n2b1 = Var("userFloat('nb1AK8PuppiSoftDropSubjets:ecfN2')", float, doc="N2 with beta=1", precision=10),
        n3b1 = Var("userFloat('nb1AK8PuppiSoftDropSubjets:ecfN3')", float, doc="N3 with beta=1", precision=10),
    )
)

run2_nanoAOD_ANY.toModify(
    subJetTable.variables,
    btagCSVV2 = Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",float,doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)",precision=10)
)

(run2_nanoAOD_106Xv2).toModify(
    subJetTable.variables,
    area = None,
    UParTAK4RegPtRawCorr = None,
    UParTAK4RegPtRawCorrNeutrino = None,
    UParTAK4RegPtRawRes = None,
    UParTAK4V1RegPtRawCorr = None,
    UParTAK4V1RegPtRawCorrNeutrino = None,
    UParTAK4V1RegPtRawRes = None,
)

run3_nanoAOD_pre142X.toModify(
    subJetTable.variables,
    btagDeepFlavB = None,
    btagUParTAK4B = None,
    UParTAK4RegPtRawCorr = None,
    UParTAK4RegPtRawCorrNeutrino = None,
    UParTAK4RegPtRawRes = None,
    UParTAK4V1RegPtRawCorr = None,
    UParTAK4V1RegPtRawCorrNeutrino = None,
    UParTAK4V1RegPtRawRes = None,
    btagDeepB = Var("bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')",float,doc="DeepCSV b+bb tag discriminator",precision=10),
)

#jets are not as precise as muons
fatJetTable.variables.pt.precision=10
subJetTable.variables.pt.precision=10

jetAK8UserDataTask = cms.Task()
jetAK8Task = cms.Task(jetCorrFactorsAK8,updatedJetsAK8,jetAK8UserDataTask,updatedJetsAK8WithUserData,finalJetsAK8)

#after lepton collections have been run
jetAK8LepTask = cms.Task(lepInAK8JetVars)

jetAK8TablesTask = cms.Task(fatJetTable,subJetTable)

import SwiftUI

struct AboutView: View {
    var body: some View {
        ZStack {
            PGBackground()
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    disclaimer
                    sources
                    Spacer(minLength: 24)
                }
                .padding(.horizontal, 20)
                .padding(.top, 12)
            }
        }
        .navigationTitle("About")
        .navigationBarTitleDisplayMode(.inline)
    }

    private var disclaimer: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("ABOUT")
                .font(PGFont.eyebrow)
                .tracking(1.8)
                .foregroundStyle(PGColors.accent)

            Text("JB Pharma is a generalist's reference for the language of pharma and healthcare — the jargon you encounter in news, earnings calls, regulatory filings, and conferences.")
                .font(PGFont.body)
                .foregroundStyle(PGColors.ink)
                .lineSpacing(3)

            Text("Entries summarize publicly available information from the authoritative sources listed below. They are written for orientation, not for clinical decision-making.")
                .font(PGFont.body)
                .foregroundStyle(PGColors.ink)
                .lineSpacing(3)

            Text("This is reference material. It is not medical advice.")
                .font(PGFont.snappyItalic)
                .foregroundStyle(PGColors.accent)
                .padding(.top, 4)
        }
    }

    private var sources: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("SOURCES")
                .font(PGFont.eyebrow)
                .tracking(1.8)
                .foregroundStyle(PGColors.accent)
                .padding(.top, 8)

            sourceGroup(
                heading: "US health agencies",
                items: ["FDA — Food and Drug Administration",
                        "NIH — National Institutes of Health",
                        "NCI — National Cancer Institute",
                        "NHGRI — National Human Genome Research Institute",
                        "CDC — Centers for Disease Control and Prevention",
                        "CMS — Centers for Medicare & Medicaid Services",
                        "HRSA — Health Resources and Services Administration"]
            )

            sourceGroup(
                heading: "International",
                items: ["WHO — World Health Organization",
                        "EMA — European Medicines Agency",
                        "ICH — International Council for Harmonisation"]
            )

            sourceGroup(
                heading: "Health economics & access",
                items: ["ICER — Institute for Clinical and Economic Review",
                        "ISPOR — Professional Society for Health Economics and Outcomes Research"]
            )
        }
    }

    private func sourceGroup(heading: String, items: [String]) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(heading)
                .font(PGFont.policyTitle)
                .foregroundStyle(PGColors.ink)
            ForEach(items, id: \.self) { item in
                Text(item)
                    .font(PGFont.body)
                    .foregroundStyle(PGColors.inkLight)
                    .lineSpacing(2)
            }
        }
    }
}

#Preview {
    NavigationStack { AboutView() }
}

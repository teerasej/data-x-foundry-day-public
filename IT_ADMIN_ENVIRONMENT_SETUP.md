# IT Admin Environment Setup for the Microsoft Foundry Agent Workshop

This guide prepares one isolated Azure and GitHub development environment per learner. Complete it before the workshop and rehearse the complete journey with an ordinary learner account on the actual workshop network.

> **Security boundary:** Give each learner one dedicated Azure resource group. Do not grant learner permissions at subscription scope, and do not reuse one cohort-wide group across every learner resource group.


## 1. Prepare the Azure subscription

> งานส่วนนี้เป็นงานระดับ subscription ของ IT Admin ครับ ผู้เรียนจะได้รับสิทธิ์เป็น Contributor ใน resource group ของตนเองเท่านั้น

ให้แน่ใจว่า subscription ที่สร้างให้กับผู้เรียนได้ register provider ที่จำเป็นทั้งหมดแล้ว:

| Service | Provider namespace |
|---|---|
| Microsoft Foundry resources, projects, and models | `Microsoft.CognitiveServices` |
| Azure AI Search and Foundry IQ | `Microsoft.Search` |
| Azure Blob Storage | `Microsoft.Storage` |
| Azure Bot Service | `Microsoft.BotService` |

## 2. สร้าง resource group ให้กับผู้เรียนแต่ละคน

1. สร้าง resource group ที่ผู้เรียนแต่ละคนจะใช้ 1 resource group ต่อผู้เรียน โดยใช้ naming convention ที่ชัดเจน เช่น `foundry-workshop-learner1-rg` หรือ `foundry-workshop-learner2-rg` เพื่อให้สามารถระบุผู้เรียนได้ง่าย
2. กำหนดเพิ่ม role และ permission ให้กับผู้เรียนแต่ละคนใน resource group ของตนเอง โดยไม่ให้สิทธิ์ในการเข้าถึง resource group ของผู้เรียนคนอื่น


## 3. Assign the 8 roles

Assign every role in this table to the learner or per-learner security group at the **dedicated resource-group scope**.

| Role | Role-definition ID | Workshop purpose |
|---|---|---|
| `Contributor` | `b24988ac-6180-42a0-ab88-20f7382dd24c` | Creates and manages learner-owned Foundry, Search, Storage, model deployment, and Bot resources. It cannot create Azure role assignments. |
| `Foundry Project Manager` | `eadc314b-1a2d-4efa-be10-5d325db5065e` | Creates and manages Foundry projects, agents, workflows, connections, and publishing operations. |
| `Cognitive Services User` | `a97b65f3-24c7-4388-baec-2e87135dc908` | Enables Microsoft Entra-authenticated inference against model endpoints inherited from the learner resource group. It does not replace Foundry roles. |
| `Storage Blob Data Contributor` | `ba92f5b4-2d11-453d-a403-e96b0029c9fe` | Creates containers and uploads, reads, and manages Foundry IQ source documents. |
| `Search Service Contributor` | `7ca78c08-252a-4471-8644-bb5ff32d4ba0` | Creates and manages Search indexes, indexers, knowledge sources, and knowledge bases. |
| `Search Index Data Contributor` | `8ebe5a00-799e-43f5-93ac-243d3dce84a7` | Loads, queries, and validates Search index data. |
| `Search Index Data Reader` | `1407120a-92aa-4202-b7e9-c0e197c71c8f` | Provides explicit read-only Search and knowledge-base retrieval access for the signed-in learner. |
| `Role Based Access Control Administrator` | `f58310d9-a9f6-439a-9e8d-f62e7b41a168` | Temporarily lets the Foundry wizard create required non-privileged managed-identity assignments inside the learner resource group. The mandatory condition is described below. |

`Cognitive Services User` and `Foundry Project Manager` serve different purposes. The first authorizes direct model-endpoint inference; the second authorizes Foundry project and agent work. Keep both assignments.

### Apply the mandatory privileged-role condition

Create the `Role Based Access Control Administrator` assignment through the Azure portal so an administrator reviews the condition visibly:

1. Open the learner's dedicated resource group.
2. Select **Access control (IAM) > Add > Add role assignment**.
3. Open **Privileged administrator roles**.
4. Select **Role Based Access Control Administrator**.
5. Assign the learner or that learner's dedicated security group.
6. Under **What user can do**, select **Allow user to assign all roles except privileged administrator roles Owner, UAA, RBAC (Recommended)**.
7. Confirm the assignment scope is the learner resource group—not the subscription or another resource group.
8. Confirm the completed assignment contains a condition and condition version.
9. Record its approved expiry or removal time.

> **⚠️ Never do this:** Do not assign this role without the condition, at subscription scope, or through a bare CLI command that omits the condition. The approved condition still permits non-privileged role assignments inside the learner resource group, so per-learner isolation and prompt cleanup are mandatory.

### Verify all learner assignments

Use an approved administrator profile. The command is read-only and should return eight learner assignments at the intended scope:

```azurecli
az role assignment list \
  --assignee-object-id <learner-or-per-learner-group-object-id> \
  --scope <learner-resource-group-resource-id> \
  --include-inherited \
  --query "[].{Role:roleDefinitionName,Scope:scope,Condition:condition,ConditionVersion:conditionVersion}" \
  --output table
```

Review the privileged assignment separately. An empty condition or a broader scope is a failed readiness check.

## 4. Verify identities created during the exercises

Roles assigned to the human learner do not authorize a service that runs as a managed identity. After the resources exist, verify these separate callers:

| Caller | Role | Target scope | Purpose |
|---|---|---|---|
| Foundry project managed identity | `Foundry User` | Associated Foundry resource | Accesses Foundry models and runtime capabilities. |
| Project or agent managed identity | `Search Index Data Reader` | Azure AI Search service | Retrieves from the Foundry IQ knowledge base at runtime. |
| Azure AI Search managed identity | `Cognitive Services User` | Foundry resource hosting the model | Calls the model for keyless Foundry IQ processing. |
| Azure AI Search managed identity | `Storage Blob Data Reader` | Exercise Storage account or Blob container | Reads source documents when the knowledge source uses managed identity. |

For the published Foundry IQ exercise, configure Azure AI Search **Security + networking > Keys > API Access control** as **Both**. The portal performs an Entra/RBAC preflight, while the exercise also uses a Search key. Do not switch to RBAC-only without adapting and rehearsing the exercise.

Treat a missing identity assignment as a rehearsal failure. Do not depend on an administrator repairing it during the live learner session.

## 5. Prepare GitHub and Codespaces

The workshop uses GitHub Codespaces as the primary environment. The repository requests 2 CPUs, 4 GB memory, 16 GB storage, Python 3.12, Git, Azure CLI, and the required VS Code extensions.

### Personal GitHub account

- Confirm the learner can sign in and open the workshop repository.
- Confirm the account has remaining included Codespaces usage or an approved payment method and budget.
- Ask the learner to create one rehearsal Codespace and stop it after validation.

### Organization-managed GitHub account

- Add the learner as an organization member or collaborator when required by repository visibility.
- Enable Codespaces for the learner under the organization's Codespaces access settings.
- If the organization will pay, use an organization-owned Codespace configuration and a nonzero Codespaces budget.
- For a private repository, provide read access plus permitted forking, or provide write access. The current workshop needs repository read access; fork or write access is required only if learners must push their work.
- Rehearse Enterprise Managed User behavior explicitly. Do not assume it matches a personal account.

GitHub documents current organization access and billing behavior in [Enabling or disabling GitHub Codespaces](https://docs.github.com/codespaces/managing-codespaces-for-your-organization/enabling-or-disabling-github-codespaces-for-your-organization) and [Choosing who owns and pays for codespaces](https://docs.github.com/codespaces/managing-codespaces-for-your-organization/choosing-who-owns-and-pays-for-codespaces-in-your-organization).

### Local fallback

If Codespaces is unavailable, prepare a managed workstation with:

- Stable VS Code and the Dev Containers extension
- Docker or another organization-approved Dev Container runtime
- Git and a supported browser
- Network access to the same Azure, GitHub, container-registry, and package-feed services
- At least the same 2 CPU, 4 GB memory, and 16 GB storage capacity

Open the repository in its Dev Container rather than recreating dependencies manually.

## 6. Validate the workshop network and learner machine

Test from the actual classroom network and ordinary learner device. Permit the minimum organization-approved access needed for:

- GitHub repository pages, authentication, Codespaces, and source downloads
- `mcr.microsoft.com` and `ghcr.io` for the Dev Container image and features
- Codespaces browser tunnels and private forwarding for port `8000`
- Azure portal, Microsoft Foundry portal, Microsoft Entra sign-in, and device-code authentication
- Foundry project and model endpoints
- Azure AI Search and Blob Storage endpoints
- Microsoft Learn MCP at `https://learn.microsoft.com/api/mcp`
- Python package installation during Codespace bootstrap

Do not maintain a copied static Codespaces domain list. Query GitHub's current metadata before the rehearsal:

```bash
gh api meta --jq .domains.codespaces
```

If a corporate firewall or TLS inspection product blocks Codespaces, review GitHub's [Codespaces connection troubleshooting](https://docs.github.com/codespaces/troubleshooting/troubleshooting-your-connection-to-github-codespaces), including the guidance for `*.visualstudio.com`.

## 7. Ordinary-learner acceptance test

Complete every check without administrator credentials in the learner browser or terminal:

- [ ] Learner can open the repository and create or open a Codespace.
- [ ] Codespace bootstrap completes and `python -m service_ops check` shows the base tools as `READY`.
- [ ] `az login --use-device-code` succeeds with required MFA or Conditional Access.
- [ ] Learner can read and modify resources only in the assigned resource group.
- [ ] Azure portal **View my access** shows all eight learner assignments.
- [ ] IT verifies the privileged assignment's scope, condition, and condition version.
- [ ] Learner can create/select the Foundry project and deploy the approved model.
- [ ] Learner can invoke the approved model with Microsoft Entra authentication and no API key.
- [ ] Foundry IQ creates Search and Storage without an **Almost there** access warning.
- [ ] Knowledge ingestion and direct learner retrieval succeed.
- [ ] The agent retrieves grounded content through its own managed identity.
- [ ] The learner cannot assign `Owner`, `User Access Administrator`, or `Role Based Access Control Administrator` and cannot assign roles outside the dedicated resource group.
- [ ] External MCP and required package feeds are reachable.
- [ ] Local MCP starts on port `8000` and a second terminal can invoke both exposed tools.
- [ ] Foundry IQ returns citations from the three synthetic knowledge documents through the portal-managed Agent.
- [ ] The visual workflow Preview and client invocation work, or the Agent Framework fallback is recorded as the approved class path.
- [ ] `SequentialBuilder` runs Summarizer, Classifier, and Resolver in order with the pinned lock file.
- [ ] If the optional extension is offered, Teams/Copilot licensing, app policy, publish scope, Azure Bot Service, and cleanup ownership are confirmed separately.

> **Workflow lifecycle:** Microsoft has announced retirement of Foundry workflows on December 1, 2026. Rehearse the visual path only while it remains available and keep Exercise 7 as the supported Agent Framework fallback.

## 8. Cleanup

1. Remove or expire the conditional `Role Based Access Control Administrator` assignment first.
2. Remove the learner's other temporary assignments.
3. Delete workshop resources according to the approved cleanup policy.
4. Stop or delete organization-funded Codespaces according to the retention policy.
5. Retain only approved audit evidence; never retain learner credentials or tokens.

## References

- [Azure built-in roles](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles)
- [Role-based access control for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Configure keyless authentication for Foundry models](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/configure-entra-id)
- [Connect Foundry IQ to Foundry Agent Service](https://learn.microsoft.com/azure/foundry/agents/how-to/foundry-iq-connect)
- [Connect to Azure AI Search using roles](https://learn.microsoft.com/azure/search/search-security-rbac)
- [Sign in with Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively)
- [GitHub Codespaces billing](https://docs.github.com/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)
